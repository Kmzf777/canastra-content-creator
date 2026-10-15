# Mercado Livre Brasil: mapa final de conhecimento

Versão final de 2026-10-15. Substitui a consolidação de 2026-10-14. É uma pesquisa neutra sobre como a plataforma funciona e como os melhores operam nela. Não parte da situação de nenhuma empresa e não traz recomendação para nenhuma.

**Para que serve.** É o ponto de partida de quem vai desenhar estratégia e agentes. Cada ponto aponta para a nota ou o arquivo de origem, onde estão a URL, o id do vídeo, o minuto e o raciocínio completo. Quando a nota e a rodada 2 divergem, vale o estado final da §12 de cada nota.

---

## Cabeçalho

### Fontes

| Camada | O que entrou | Contagem |
|---|---|---|
| Notas de frente | 8 notas (ads, preço, logística, ranqueamento, mix, reputação, alimentos, cases), cada uma com tabela de afirmações e §12 de estado final | 8 notas, 280 linhas de estado final |
| Vídeos (YouTube) | `videos.tsv` (listados), `selecionados.tsv` (escolhidos), `transcricoes/` | 313 listados, 91 selecionados, 87 transcritos |
| Webinars oficiais (rodada 2) | Canal "Vendedores Mercado Livre Brasil", lidos com minuto | 12 vídeos (nov/2025 a set/2026) |
| Social | Reels e TikTok transcritos; legendas; títulos só como indício | 23 transcrições (1 duplicada), 40 legendas, 12 títulos |
| Observação direta | 14/10: 13 páginas de líderes (CEP em MG). 15/10: 6 termos × 24 posições, mais uma 2ª passada | 13 páginas; 168 linhas |
| Verificação de páginas oficiais | `verificacao/resultado-mercadolivre.tsv` (seções 10 e 11 das notas) | 46 linhas: 27 confirmadas, 16 parciais, 1 contestada, 2 sem fonte |
| Balanços e documentos públicos (N2) | 4 cartas (3T25 a 2T26), 4 calls (transcrição de terceiro), 10-Q 2T26; Anvisa, DOU, Planalto, INPI, MAPA, Procon-SP | 35 achados regulatórios (R2-REG-1 a 35); 30 de balanço e API (R2-BA) |
| Estudos e dados (N4/N5) | NIQ Ebit, Worldpanel, ABIC, Lett, Nubimetrics, literatura acadêmica | 28 achados de dados (R2-DAD); 29 de evidência e cases (R2-EVC) |

### Nível de verificação (estado final, §12.1 das 8 notas)

Algumas linhas da §12.1 agrupam mais de um id. Por isso a contagem é por linha.

| Status final | Linhas | O que significa |
|---|---|---|
| CONFIRMADA | 137 | Cerca de 100 por texto escrito do ML (N1). Cerca de 14 por N2 ou estudo (SEC, Anvisa, DOU, NIQ). 16 só por fala oficial em vídeo, sem página escrita. 5 por observação direta. 1 de outra plataforma (Amazon EUA, fora do ML). |
| PARCIAL | 38 | Parte confirmada, parte sem fonte, ou duas fontes oficiais em conflito |
| CONTESTADA → valor corrigido | 11 | A fonte oficial diz outra coisa. O valor correto está na nota e nesta versão. |
| SEM FONTE OFICIAL | 71 | Prática, case autodeclarado ou dado sem método. Na maioria, não é verificável por natureza. |
| ABERTA | 22 | Sem releitura, ou com fonte oficial sem evidência |
| Sem mudança (observação + prática) | 1 | — |

Na integração da rodada 2, as frentes atualizaram 196 afirmações: ads 19, preço 23, logística 38, ranqueamento 31, mix 21, reputação 14, alimentos 20, cases 30.

**Contaminação.** Só uma linha foi descartada. É a linha A12 da seção 10 de alimentos, que citava o Subscribe & Save da Amazon EUA sob o id de uma afirmação sobre o Brand Protection Program do ML. Essa leitura foi reatribuída a [alim A19], que trata da Amazon, e não foi usada como evidência do ML [alim §12.5]. Nenhuma outra frente achou contaminação. As menções a Amazon e Shopee na rodada 2 vêm rotuladas como tal e não sustentam nenhuma afirmação sobre o ML.

### O que mudou desde a versão de 14/10

1. **Desconto de envio por reputação:** 50% no verde (embutido), 40% no amarelo, 0% no laranja e no vermelho; os 70% estão superados [rep A15; R2-SIN-9, 10].
2. **Reputação:** desde 10/09 (ano inferido 2026), a janela de 60 dias exige 101 vendas em 60 dias (antes, 60); o "68" é erro. Há tabela oficial por cor para 365 dias [rep A2, A4].
3. **Custo fixo:** desde 02/03/2026, só Flex, ME1 e envio personalizado cobram abaixo do TH. A nota com "50% abaixo de R$12,50" é a regra anterior [mix A37; R2-BA-5].
4. **Tarifa do café:** 14% e 19%. A redução da 51251 vale também para Cápsulas, Solúvel, Infusões e Cremes [pre A1, A8].
5. **Custos do Full lidos em texto:** armazenagem do Supermercado, isenções, retirada, descarte e estoque antigo [log A1–A3, A26].
6. **Supermercado no Full:** a 23329 restringe alguns produtos, não a categoria; a lista não é pública [alim A3].
7. **Experiência de compra:** 60 dias com 100 vendas, senão o último ano; os 180 dias são janela de exibição [rank A9].
8. **Price matching:** duas modalidades (uma 100% ML) e até 10 dias; a lista de promoções bonificadas foi corrigida [pre A14, A19].
9. **Product Ads:** Ad Score × CPC só existe por escrito para Brand Ads; requisitos com conflito entre texto e fala [ads A4, A6].
10. **Busca com protocolo:** patrocinados nas posições 1–4 e 13–16; em café, 83–92% do topo é Full Super [R2-OBS-2, 5].
11. **Causalidade rebaixada:** o México teve o mesmo crescimento do Brasil no 3T25 sem o frete desde R$19 [cases A5; R2-EVC-15].
12. **Correções de N2:** +56% de itens é do 2T26; +1,1 p.p. de conversão é do Brasil; 1P abaixo de 10% do GMV; "Basics" sem fonte [log A19; R2-BA-18, 28; alim A28].
13. **Regulatório lido na fonte:** café na via comunicação da IN 281; 01/09/2026 não é prazo do café; classe 30 sem regra de classe no ML; o 0,34% de Cajamar é declaração do ML [alim A13–A16, A27].
14. **API pública fechada:** busca, tendências e `listing_prices` exigem token [rank A34; R2-BA-20 a 26].
15. **"60 dias antes da Black Friday"** é recomendação do Procon-SP, não lei [R2-REG-25, 26].

### Como ler as citações

| Código | Arquivo |
|---|---|
| [ads] [pre] [log] [rank] [mix] [rep] [alim] [cases] | `ads/`, `preco-promocao/`, `logistica-estoque/`, `ranqueamento-anuncio/`, `produto-mix/`, `reputacao-atendimento/`, `alimentos-marca-propria/`, `cases-grandes/` (sempre `notas.md`) |
| [soc] | `social/notas.md` |
| [obs] | `observacao/lideres.md` |
| R2-REG / R2-BA / R2-WEB / R2-DAD / R2-EVC / R2-SIN / R2-FS / R2-PR / R2-OBS | `rodada2/regulatorio.md`, `balancos-api.md`, `webinars.md`, `dados-mercado.md`, `evidencias-cases.md`, `sinais-recentes.md`, `nav-full-supermercado.md`, `nav-preco-reputacao.md`, `nav-observacao.md` |

"[rep A3]" é a afirmação A3 da nota de reputação. O estado final está na §12.1 da nota. "[log §2.3]" é a seção 2.3. Níveis de fonte (protocolo §2): N1, documento oficial; N2, balanço ou órgão público; N3, observação; N4, estudo com método; N5, ferramenta de estimativa; N6, praticante com tela; N7, curso sem demonstração; N8, comentário. Confiança: A, B ou C (protocolo §3).

**"Pode estar superada".** Nenhuma página da Central de Ajuda nem da Central de Vendedores traz data. Toda regra lida nelas vale como "vigente na leitura de 14 e 15/10/2026". Fala oficial anterior a 14/04/2026 também leva a marca.

---

## 0. A plataforma em uma página

### Como o dinheiro circula

**O que o vendedor paga em cada venda**
- **Tarifa:** Clássico 10–14% ou Premium 15–19%, este com parcelas sem juros; no café, 14% e 19% [pre A1; R2-PR-1]. O percentual pode variar no tempo [R2-BA-6].
- **Envio em toda venda**, por peso e faixa de preço; abaixo de R$19, no máximo metade do preço [pre A2–A4].
- **Custo fixo** desde 02/03/2026 só no Flex, no ME1 e no envio personalizado, abaixo de um limite (TH) não publicado [mix A37; R2-BA-5].
- **No Full:** armazenagem, estoque antigo, inconformidade, retirada e descarte [log A1–A6, A26].
- **Fora do repasse:** publicidade, custos do Full e Minha Página; o ML não retém impostos [R2-PR-21].

**Frete grátis**
- De R$19 a R$78,99, o ML oferece frete grátis padrão (lento). A partir de R$79, o vendedor oferece frete grátis rápido [pre A6].
- Assinantes do MELI+ têm entrega rápida desde R$19 (out/2025). O plano Essencial custa R$9,90 por mês [cases A31; R2-BA-8].
- O frete grátis lento tem contribuição variável positiva em metade das faixas de R$19 a R$79 (2T26) [R2-BA-11].
- Divergência oficial aberta: a ajuda/16449 diz "fora da loja, frete grátis a partir de R$79" [R2-BA-29].

**A plataforma paga por preço competitivo (N2)**
- Desde abril de 2026, há desconto no Pix ao comprador e desconto de tarifa ao vendedor. Valem "em certas categorias e faixas de preço" e dependem de preço competitivo [pre A9; cases A1].
- A tarifa de envio do vendedor caiu no fim do 1T26 [R2-BA-13].
- Os "−1 p.p." e a "armazenagem grátis no Full" só aparecem na imprensa [cases A2].
- O ML compara preços com concorrentes "internos ou externos" e oferece automação que considera outros sites e o Google [cases A3; pre A23]. A punição com aviso e prazo de 3 dias só aparece na imprensa [R2-SIN-18].

### O que decide quem vende

Os fatores estão em ordem de força da evidência. O ML não publica fórmula nem pesos [rank §12.4 Q1].

1. **Reputação da conta é porta de acesso.** A cor define o desconto de envio (50%, 40% ou 0%), o acesso ao Product Ads e à automação no catálogo (amarela ou melhor), a vitória no catálogo (laranja e vermelha não ganham) e o acesso a cupons, Full Super e estoque compartilhado (só verde) [rep §12.4 Q2; rank A4]. A medalha dá "mais visibilidade", sem medida do efeito [rep A38].
2. **Experiência de compra por anúncio.** É uma nota de 0 a 100. A nota Mediana tira exposição e pode pausar o anúncio; a Ruim pode cancelá-lo. Entram reclamações, atrasos, perguntas e inconsistências do anúncio [rank A8; rep A18].
3. **Logística.** O Full está entre os critérios do catálogo [rank A4]. Também entra no Ad Score do Product Ads, segundo fala oficial [R2-WEB-1]. A ajuda/16449 promete "destaque nas buscas" para a loja Full Super [rank §12.2]. Em café, o topo da busca é quase todo Full Super [R2-OBS-5].
4. **Preço total e condições no catálogo.** O vencedor é escolhido por algoritmo: preço, parcelas sem juros, Full, frete grátis e envio no mesmo dia. Quem vence leva visibilidade máxima; quem perde, mínima [rank A4–A6]. Há observação de anúncio a R$141 no Full que ganhava de outro a R$139 [rank A40, prática].
5. **Qualidade do anúncio.** É uma nota de 0 a 100. Entram GTIN, ficha técnica, fotos, título, frete grátis, parcelas, estoque e tempo de disponibilidade [rank A12, A13; página de 31/01/2025, pode estar superada].
6. **Ads.** Um terço das 24 primeiras posições é patrocinado, em slots fixos [R2-OBS-2]. O leilão considera ROAS objetivo e relevância; a reputação entra na "qualidade", segundo fala de set/2026 [ads A4; R2-WEB-3]. Que Ads eleve o orgânico é afirmação oral do ML, sem teste [rank A42].

### Para onde a plataforma vai (N2)

- **Ads:** +62% a/a no 2T26 (+63% no 3T25 e no 1T26), com mais de 10% da publicidade digital da América Latina. A relação Ads/GMV não é divulgada [ads A34; R2-BA-15, 16].
- **IA em Ads:** a adoção do orquestrador de orçamento cresceu 63% contra o trimestre anterior. O assistente de Ads no WhatsApp atende "dezenas de milhares" de vendedores por mês [ads A35].
- **1P:** menos de 10% do GMV, com mais de US$4 bi em 2025 (+80%). Preenche lacunas de seleção ou preço [R2-BA-18, 19].
- **MELI+:** assinantes +72% a/a [R2-BA-10].
- **Fulfillment:** 55% dos envios regionais e mais de 50 instalações. O número do Brasil não é divulgado [log A18].
- **API:** os dados de mercado ficaram atrás de token e permissão. Apps só de leitura podem ser bloqueados [R2-BA-20 a 26].

**Leitura.** A plataforma premia preço total competitivo, entrega rápida e poucos problemas por anúncio. Ela vende exposição paga em slots fixos e compete em 1P onde falta seleção ou preço.

---

## 1. Regras e números que importam

Só entram regras oficiais, com o status final. As páginas sem data valem como lidas em 14 e 15/10/2026. "Fala" quer dizer vídeo ou webinar oficial sem página escrita.

| Tema | Regra / número (valor final) | Fonte | Data | Status | Nota |
|---|---|---|---|---|---|
| Tarifa | Clássico 10–14%, sem parcelas; Premium 15–19%, até 12x. Escada de parcelas: R$30–59,99 2x; R$60–99,99 3x; R$100–149,99 4x; R$180–299,99 6x | ajuda/870; 22737 | s/d | CONFIRMADA | [pre A1; R2-BA-7] |
| Tarifa café | Café Moído e em Grão (MLB247538): Clássico 14%, Premium 19% | landing custos-de-venda (buscador) | s/d | CONFIRMADA, média-alta (leitura única, sessão logada) | [pre A1; R2-PR-1] |
| Tarifa reduzida | R$150–700: −3 p.p. Clássico e −5 p.p. Premium em Café, Moído e Grão, Cápsulas, Solúvel, Infusões e Cremes. Café nessa faixa: cerca de 11% e 14% (inferência) | ajuda/51251 | s/d | CONFIRMADA, ampliada | [pre A8; R2-BA-4; R2-PR-3] |
| Tarifa Supermercado | "Pagam outras tarifas", sem percentual público | ajuda/870 → 16449 | s/d | PARCIAL | [cases A29] |
| Custo fixo | Desde 02/03/2026, abaixo do TH: só Flex (ME2), ME1 e personalizado. Full, Coleta, Places, Drop off e Turbo não cobram. Acima do TH, nenhum. TH não publicado | developers "Custos por vender" | 03/09/2026 | CONTESTADA → corrigido (lido por uma frente; desempate por WebFetch deu 403) | [mix A37; R2-BA-5] |
| Envio | Em toda venda. Até 0,3 kg: 5,65 / 6,85 / 8,15 / 12,95 / 14,95 / 16,95 / 19,05 / 21,65 nas 8 faixas (de R$0–18,99 a R$200+). 0,3–0,5 kg a R$19–48,99: R$6,95. 0,5–1 kg: 6,05 / 7,15 / 8,45 / 14,45 nas 4 primeiras faixas. Abaixo de R$19: no máximo metade do preço | ajuda/40538 | s/d | CONFIRMADA | [pre A2–A4; alim A8] |
| Envio × reputação | Verde, Líder ou sem reputação: até 50%, já embutido. Amarela: até 40%. Laranja e vermelha: 0% (até 0,3 kg a partir de R$79: R$25,90 contra R$12,95) | ajudas 40538, 40545, 40547 | s/d | CONFIRMADA (70% superado) | [rep A15; log A11] |
| Frete grátis | R$19–78,99: padrão, pago pelo ML. A partir de R$79: rápido, pago pelo vendedor. Rápido opcional abaixo de R$79, a partir de R$12,95 | ajuda/40538 | s/d | CONFIRMADA; conflito com "R$79 fora da loja" da 16449 | [pre A6; log A10] |
| Tabela nova | "Custos do Envios a partir de 24 de agosto" (ano inferido). "+1,6%" sem fonte; e-mail em vídeo cita cerca de R$0,90 por envio | ajuda/48578 | s/d | PARCIAL | [pre A7; R2-SIN-29] |
| Kit | Tarifa de cada produto e um envio por kit. No Supermercado não há economia por quantidade nem por kit | 870; 40538; 45023 | s/d | CONFIRMADA | [mix A7; alim A9; pre A12] |
| Promoções | 12 tipos. Com bonificação do ML: MARKETPLACE_CAMPAIGN, VOLUME, PRE_NEGOTIATED, SMART, PRICE_MATCHING, UNHEALTHY_STOCK. Sem: DEAL, DOD, LIGHTNING, SELLER_CAMPAIGN. *Boost* automático do ML compensado em custos; aporte separado por `meli_percentage` e `seller_percentage` | developers gerenciar-ofertas | 09/06/2026 | PARCIAL (lista corrigida) | [pre A14, A15] |
| Promoções | VOLUME: a tabela de 2026 marca bonificação, a doc de 2025 diz que não há | idem; doc Volume | 2026 × 2025 | ABERTA | [pre A18] |
| Price matching | PRICE_MATCHING cofinanciado; PRICE_MATCHING_MELI_ALL 100% ML; até 10 dias (SMART: 30); compara com outros sites; candidatos diários | developers smart-price-matching | 09/06/2026 | CONTESTADA → corrigido | [pre A19; rank A31] |
| Cupom | Só reputação verde; até 31 dias; acumula com promoção; um por venda | developers cupons | 28/08/2025 (pode estar superada) | CONFIRMADA | [pre A17] |
| Automação de preço | INT ou INT_EXT (fora do ML, inclui Google); `min_price` obrigatório; validação contra 60 dias; PUT de preço ignorado desde 18/03/2026; pausa quando o item entra em promoção; no catálogo, amarela ou melhor | developers automatizacoes-de-precos | 01/10/2026 | CONFIRMADA | [pre A23; R2-PR-18] |
| Preço de referência | Compara com concorrentes internos e externos. `max_discounted_price` limita o desconto a "descontos críveis"; critério não publicado | developers referencias-de-precos; gerenciar-ofertas | 17/12/2025; 09/06/2026 | CONFIRMADA (existência) | [pre A22, A24; R2-REG-35] |
| Preço externo | Aviso, prazo de 3 dias e perda de visibilidade e Ads | imprensa | 24/10/2025 | OFICIAL via terceiro | [cases A3; R2-SIN-18] |
| Desconto por quantidade | Verde ou amarela; experiência ≥50; até 1 mês; produto novo; não vale para itens por kg nem kits | nota; developers | 23/01/2025 (pode estar superada) | CONFIRMADA | [mix A8] |
| Atacado | Só para CNPJ; frete até 80% menor, exceto volumosos e Supermercado | nota | s/d | CONFIRMADA | [mix A9] |
| Full: armazenagem | Por unidade e dia: P R$0,007, M 0,015, G 0,050, XG 0,107. Supermercado: P e M grátis, G 0,014, XG 0,025. Vale para aptas e não aptas | envios Full; ajuda/24253 | s/d | CONFIRMADA | [log A1; alim A5] |
| Full: estoque antigo | Geral a partir de 4 meses: P R$1/12/28; M 2/15,90/35; G 6/40/92; XG 8/52/145 (4–6, 6–12, >12 meses). Supermercado a partir de 2 meses: P 2,00/4,40/9,20/14,20, até XG R$83,50 | ajuda/15373 (mesma tabela na 15731) | s/d | CONFIRMADA (não há "+6,4%") | [log A2, A3, A34; alim A4] |
| Full: isenções | Extraviadas, em revisão, devolvidas, canceladas, em transferência. Extraviada não recuperada em 30 dias é paga | ajuda/26342 | s/d | CONFIRMADA | [R2-FS-12] |
| Full: retirada e descarte | Retirada R$98 até 0,01 m³, caindo a cerca de R$1.121/m³ (1–2 m³) e R$576–583/m³ acima de 20 m³. Descarte de R$1 a R$18/m³ | ajuda/16645 | s/d | CONFIRMADA, com 2 incoerências internas | [log A26] |
| Full: índice | 40/30/20/10; a nota do dia 15 define o espaço do mês seguinte; 70 ou mais dá espaço estendido; estrelas ficam fora de 3 métricas. A isenção de até 180 dias do estoque antigo para estrelas só existe em fala | nota; tGWTaeqbsmU | s/d; 23/07/2026 | CONFIRMADA; 180 dias PARCIAL | [log A4, A5; mix A12] |
| Full: inconformidade | R$5 / R$3 / R$9 por unidade; tolerância de 5%. Abono trimestral só para cancelamento tardio e não comparecimento | nota | s/d | CONFIRMADA | [log A6] |
| Full: entrada | Menos de 25 kg, um lado até 120 cm, soma até 260 cm; validade acima de 90 dias. Extragrandes por lista: ≥20 kg, ≥80 cm ou ≥125 L, com exceção por preço (R$100 ou R$200). Nenhuma categoria de alimentos na lista | 15573; 44922 | s/d | CONFIRMADA (data 20/05 sem fonte) | [log A7, A9] |
| Full: proibidos | Controle de temperatura ou umidade; kit ou pack de supermercado sem EAN; consumo recorrente com validade próxima; validade ilegível ou manuscrita; lista sem condição de tamanho | ajuda/5200 | s/d | CONFIRMADA | [log A8, A38; alim A2] |
| Full: ruptura | Sem estoque no CD, o anúncio pausa; dá para desvincular o Full e vender por Flex | nota Flex+Full | s/d | CONFIRMADA | [log A12] |
| Anúncio por envio | É permitido o mesmo produto em outro anúncio para outra forma de envio ou pagamento | ajuda/2517 | s/d | CONFIRMADA | [rank A22] |
| Estoque compartilhado | Verde; experiência ≥75; catálogo; EAN impresso; sem validade. Exclui Alimentos e Bebidas. Ninguém responde por produto de outro vendedor | 42158; 42159 | s/d | CONFIRMADA | [log A22; alim A32] |
| Despacho | Envios com problema no verde: até 10% (60 d) e 13% (365 d). "Chegará amanhã": 97% no prazo. Bônus Flex de 10% a partir de R$79, só no verde | notas | s/d | CONFIRMADA | [log A23, A24] |
| Supermercado | A 23329 restringe alguns produtos a autorizados e não aceita novos; lista não pública. As categorias excluem preparados, congelados, refrigerados, instantâneos, embutidos e confeitaria | 23329; 5200; 33536 | s/d | CONFIRMADA (escopo por inferência média) | [alim A3; R2-FS-1 a 5] |
| Full Super | Preço acima de R$8; verde; estoque no Full; P e M sem armazenagem; frete grátis na loja a partir de R$199; exceções por marca | ajuda/16449 | s/d | CONFIRMADA | [alim A6; log A21] |
| Full Super: envio | Abaixo de R$29: no máximo 25% do preço. "Selecionados" × demais: R$1,60 × R$2,40 (R$29–48,99) e R$2,40 × R$3,60 (R$49–78,99). Diferença só até 8 kg; iguais a partir de R$199; automático para anúncio de catálogo. Lista em PDF não lida | ajuda/49972 | s/d | CONFIRMADA (valores); PARCIAL (critério, data e rótulo de peso) | [pre A11; alim A7; log A25] |
| Reputação: janela | Cinza até 10 vendas em 365 d. Desde 10/09, com 101 vendas ou mais em 60 d vale a janela de 60 d; senão, 365 d | ajuda/866; nota "vamos mudar…" | s/d (ano inferido 2026) | CONFIRMADA | [rep A1, A2] |
| Reputação: cores | 60 d (verde / amarelo / laranja): reclamações 2 / 4,5 / 8%; canceladas 1,5 / 3,5 / 4%; envios incorretos 10 / 18 / 22%. 365 d: canceladas 2,5 / 5,5 / 6,5%; envios 13 / 23,5 / 28,5%; reclamações iguais | nota "vamos mudar…" | s/d | CONFIRMADA | [rep A3, A4, §12.1] |
| MercadoLíder | Líder / Gold / Platinum: 230 / 575 / 1.725 vendas e R$37.000 / 118.400 / 296.000 em 3 meses mais o mês corrente. Reclamações <1%; mediações e canceladas <0,5%; envios <6%; mais de 4 meses de conta | ajuda/864 | s/d | CONFIRMADA | [rep A5–A6] |
| O que conta | Só reclamação de produto (pacote avariado não). Arrependimento não conta. Mediação só pesa no Líder. Acima de 2,5% de canceladas a conta "poderá ser suspensa". `has_incentive` com resposta em 48 h não afeta | 30193; 5205; developers | s/d | CONFIRMADA | [rep A7–A11] |
| Programas | Decola: R$250, até 365 d, 5 vendas afetadas. Protegida: 1–3% do faturamento de 60 d, por 60 dias corridos; reativação só 6 meses depois; aceita verde com anúncios amarelos ou vermelhos. "Benefício de Reputação" é provavelmente o mesmo programa | 33314; 29276; 29528 | s/d | CONFIRMADA; equivalência ABERTA | [rep A21–A23] |
| Devolução | 30 d (novo) ou 5 d (usado). Arrependimento é grátis para o vendedor e não afeta; defeito ou diferença custa e pode afetar | 3285; 28088; 32761 | s/d | CONFIRMADA | [rep A24–A25] |
| Experiência de compra | Boa 75–100, Mediana 50–74, Ruim ≤30 (31–49 sem classe). 100 vendas em 60 d, senão o último ano; abaixo de 100, completa pela categoria (200 vendas). Congelamentos "Benefício" e "Verde claro". Kit herda a pior nota | nota; developers; 39234 | 03/02/2026 | CONFIRMADA (180 d = exibição, por leitura cruzada) | [rank A8, A9, A11; rep A18–A20] |
| Catálogo | Preço, parcelas sem juros, Full, frete grátis, mesmo dia. `winning` / `sharing_first_place` / `competing` = visibilidade max / medium / min. Laranja e vermelha não ganham. Vencedor depende de localização. `price_to_win` | developers concorrencia-em-catalogo | 21/07/2026 | CONFIRMADA | [rank A4–A6; cases A27] |
| Qualidade | 0–100, níveis Básica, Satisfatória e Profissional | developers | 31/01/2025 (pode estar superada) | CONFIRMADA | [rank A12, A13] |
| Anúncio | Título de 60 caracteres (também nas folhas de café, que têm preço mínimo de R$8); 12 fotos (10 por variação); descrição até 50.000; foto 1200×1200 recomendada, mín. 500, máx. 1920, 10 MB, 95% do espaço | API /categories; developers | 14–15/10/2026; 24/03/2026 | CONFIRMADA | [rank A14–A16; R2-BA-3] |
| Duplicados | Proibidos. Três tratamentos escritos: cancelado, ocultado ou excluído com possível desativação da conta. Usar variações | nota; ajuda/2517 | s/d | CONFIRMADA | [rank A21; mix A3] |
| Edição | Pela API, título não editável com vendas. Fala oficial diz o contrário e que a edição faz o anúncio ser "lido como novo" | developers sincronização; MFYKfOYs0iE | 24/03/2026; mai/2026 | PARCIAL | [rank A20] |
| Clips | Texto: 9:16, de 10 s a 1 min. Fala: aprovação em até 48 h; até 280 MB; ilimitados; logo abaixo de 10%; proibidos contato, preço, imagem estática e música de terceiros | nota; vídeos oficiais | s/d; jan–mai/2026 | CONFIRMADA (texto + fala) | [rank A23, A27, A29] |
| Kit virtual e UP | Kit virtual: 2 a 6 produtos, composição imutável, só item novo. User Products: preço e condições por variação, até 30 | developers | 17/09/2026 | CONFIRMADA | [mix A5, A6] |
| Ads: métrica | Product Ads por ROAS objetivo de 1x a 35x; ACOS = 1/ROAS; `acos_target` só até 30/03/2026 | developers PAds | 06/07/2026 | CONFIRMADA (com ressalva de leitura) | [ads A1–A3] |
| Ads: leilão | Escrito: ROAS objetivo + relevância. Ad Score × CPC escrito só para Brand Ads. Fala: Ad Score (título, avaliação, Full, foto, posição) × CPC; em set/2026, qualidade (com reputação), relevância e ROAS. "Segundo preço" com fonte oral única | nota Central; developers Brand Ads; JzejZyVeauE; LOZL-QmsGL4 | 09/06/2026; mai e set/2026 | PARCIAL | [ads A4, A5; rank A30] |
| Ads: requisitos | Texto: amarela (a partir de 10 vendas), sem dívidas, sem restrição, ≥1 anúncio ativo; o Decola dispensa a reputação. Fala (3 webinars de 2026): 15 dias de conta e sem fatura vencida | nota Central; webinars | s/d; 2026 | CONFIRMADA (texto); divergência ABERTA | [ads A6; rep A16] |
| Ads: cobrança | Só por clique, na fatura do Mercado Pago; display e vídeo por impressão | fala; 10-Q 2T26 | 2026 | CONFIRMADA | [ads A17] |
| Ads: atribuição | 14 dias (texto) × 15 dias (fala de maio) | developers; JzejZyVeauE | 06/07/2026 | PARCIAL | [ads A10] |
| Ads: ferramentas | Métricas `sov`, impression share e impressões perdidas por orçamento e por classificação. Redistribuição automática de orçamento (exclui campanhas com menos de 7 dias). Teste grátis de 10 dias (20 no Meli Pro). ROAS Dinâmico (set/2026) | developers; notas; fala | 2026 | CONFIRMADA | [ads A11–A15; R2-WEB-21, 22] |
| Brand Ads | Loja oficial ou Minha Página; verde; ≥3 publicações; campanha de 3 a 10 itens e 1 a 200 palavras-chave. Migração para Product Ads desde 17/06/2026, para um grupo não público | developers | 09/06/2026 | CONFIRMADA | [ads A8, A9] |
| Catálogo × Ads | Product Ads de catálogo só imprime para quem vence o catálogo | fala b-ZNQktRHjc | nov/2025 (pode estar superada) | PARCIAL | [ads §12.1; R2-WEB-18] |
| API | Busca, tendências, mais vendidos, visitas e `listing_prices` exigem token e permissão ("Métricas do negócio", "Publicidade"). Estoque público em faixas. App só de leitura pode ser bloqueado. Scraping proibido | developers; curl | 2025–2026 | CONFIRMADA | [rank A34; mix A10, A18] |
| Alimentos | Proibidos: sem inscrição sanitária, aberto ou fracionado, perto do vencimento; "Artesanal" em destilados | ajuda/Alimentos_2274 | s/d | CONFIRMADA | [alim A10] |
| Alimentos no Full | Validade acima de 90 dias, rótulo em português, Anvisa ou MAPA. A página cita a RDC 259/2002, já revogada | ajuda/15737 | s/d | CONFIRMADA | [alim A1; R2-REG-18] |
| Marca | Loja oficial: registro vigente no INPI, sem protocolo; Minha Página; sem exclusividade; não cita classe. BPP gratuito, com certificado | nota Lojas Oficiais; 1087; FAQ BPP | s/d | CONFIRMADA | [alim A11, A12] |
| MELI+ | Termos excluem Supermercado e Compras Internacionais; subsídio de até R$20 de frete | ajuda 30487 | s/d | CONFIRMADA | [cases A31] |

---

## 2. Por frente: o que os melhores fazem

Em cada frente, "regra" é N1 ou fala oficial, e "prática" é praticante (N6/N7), quase sempre com confiança C. Nenhuma prática tem teste controlado público.

### 2.1 Ads

- **Meta a partir da margem** (método aritmético, consenso) [ads A22; pre A30]:
  - ACOS máximo = margem antes de Ads (CM1%);
  - ROAS mínimo = 1 ÷ CM1;
  - a meta prática fica abaixo do equilíbrio.
- **ROAS por fase** (prática) [ads A23]: lançamento de 2 a 5, escala de 5 a 10, rentabilidade de 10 a 25. As falas oficiais divergem no ponto de partida: ROAS 10 (casos de 3 a 40), ROAS 5 e "siga o recomendado" [ads A24]. No social, as receitas iniciais vão de 15 a 25 de ROAS [soc S03–S04].
- **Estrutura:** agrupar por margem, ROAS e curva ABC, sem misturar conversões muito diferentes (fala oficial e prática) [ads A27; mix A15]. O ML recomenda de 15 a 30 produtos por campanha, como orientação e não como limite [ads A18].
- **Produto novo:** tem "score pior", não entra em campanha em andamento e fica de 20 a 30 dias numa campanha nova (fala oficial, fonte única) [ads A19].
- **Ritmo de ajuste:** 7 dias sem mexer é "regra de ouro" em duas falas de set/2026 [ads A25]. O primeiro ajuste em 15 a 20 dias e o ROAS +2 a cada 7 a 15 dias são prática.
- **Peneira** [ads A26]: de 10 a 20 anúncios em teste; os 3 ou 4 que levam os cliques vão para a campanha principal.
- **Estoque e Ads** (oficial): com estoque baixo na variação, subir o ROAS e isolar o produto, em vez de cortar o orçamento [ads A30]. O orçamento diário é teto, não meta [R2-WEB-29].
- **Régua da conta:** TACOS de 1,5% a 6% (prática) [ads A28; soc S06]. É atribuição tratada como causa.
- **Leitura de concorrência:** o painel Concorrência mostra o % de vendas com publicidade de cada concorrente [ads §12.2]. A observação de busca mostra 8 de 24 posições pagas e um banner de marca [R2-OBS-2, 3].
- **Contraponto:** há operação que declara cerca de R$1,5 milhão em 30 dias sem Ads [soc S07]. O consenso é que Ads amplifica o que já converte.

### 2.2 Preço e promoção

- **Preço-alvo de trás para frente** [pre §3.4; soc S09]: P = (custo + embalagem + envio) ÷ (1 − tarifa − imposto − TACOS − devoluções − margem). O cálculo é iterativo, porque o envio muda com a faixa de preço. A escada é CM1, CM2 (depois de Ads) e CM3 (depois de Full, devolução e cupom).
- **Degraus de envio:** baixar o preço de R$50,49 para R$48,99 muda a faixa (prática) [soc S12]. Com o fim do custo fixo no Full e na Coleta, o peso no ticket baixo vem do envio, que é no máximo metade do preço abaixo de R$19 [mix A21].
- **Preço de lista com espaço para campanha:** uma operação tinha 81% dos anúncios em cofinanciadas [pre A25]. O limite oficial é que `max_discounted_price` restringe o desconto a valores "críveis" [pre A22].
- **Cobertura contínua de promoções** [pre A28]: promoção e cupom se somam (oficial). "Só a de maior desconto fica ativa" é prática.
- **Prioridade às cofinanciadas.** O ML banca parte em seis tipos de promoção e 100% no PRICE_MATCHING_MELI_ALL [pre A14, A19].
- **Piso explícito:** margem-alvo de cerca de 20% (prática). A automação oficial exige `min_price` e pausa quando o item entra em promoção [pre A23].
- **Evitar guerra de preço** [pre §12.4 Q7]: piso na automação, opção de não acompanhar o price matching, kits, linha de formatos e a faixa de tarifa reduzida de R$150 a R$700.
- **Medir competitividade:** não há prática documentada de índice de preço par a par nem de buy box por portfólio [pre §12.4 Q4]. O painel Concorrência mostra o uso de alavancas, não preço relativo.
- **Moldura legal do "de/por"** [R2-REG-25 a 29]:
  - publicidade enganosa inclui preço, e o ônus da prova é do anunciante (CDC, arts. 37 e 38);
  - preços distintos para o mesmo item são infração (Decreto 5.903);
  - o Procon-SP recomenda calcular o desconto sobre o menor preço de 60 dias.

### 2.3 Logística e estoque

- **O que vai para o Full:** curva A e estrelas, com a curva ordenada por unidades; testes e baixo giro ficam em Flex ou Coleta; produto novo vai em lote pequeno [log §3.1, A28].
- **Custo de manter:** o descarte é muito mais barato que a retirada [log A26]. No Supermercado, o estoque antigo começa aos 2 meses [log A2].
- **Cobertura:** 4 a 8 semanas na referência oficial em vídeo; os praticantes enviam para 15 a 30 dias e revisam a cada 15 [log A14, A30].
- **Lead time completo:** a disponibilidade no CD pode levar até 2 semanas (fala oficial). O estoque de segurança fica no depósito próprio [log A16].
- **Índice do Full acompanhado todo dia**, porque a nota do dia 15 define o espaço [log A4].
- **Ruptura:** o anúncio pausa (oficial). A recomendação de reposição cai, segundo vídeo oficial. Não há tempo de recuperação medido no ML [log A12, A13; §12.4 Q7].
- **Black Friday** (prática): planejar desde meados de setembro, fechar envios até 20–25 de outubro, de 10 a 20 SKUs [log A31, A32].

### 2.4 Ranqueamento e anúncio

- **Cadastro completo antes de tráfego:** ficha técnica, de 5 a 8 fotos com função, clipe e descrição [rank §3.1]. Sem vídeo, a qualidade não chega a 100% (fala) [rank A24].
- **Palavra-chave tirada do ML:** autocomplete, "mais buscadas", Tendências e Análise de concorrência; produto nas primeiras palavras do título [rank §12.4 Q3].
- **Clips:** vários por produto, porque cada usuário vê um clipe uma vez. No catálogo, o da marca aparece primeiro [rank A23–A28].
- **Mexer no anúncio vencedor:** a fala oficial diz que o anúncio é "lido como novo", sem página nem dado [rank A20].
- **Funil** (prática) [rank A38; soc S22]: impressão baixa aponta relevância; clique baixo, capa, preço e título; visita sem venda, preço total e confiança. A Análise de concorrência e as métricas do Ads sustentam o diagnóstico.
- **Catálogo:** monitorar `price_to_win` e reagir com logística, parcelas e preço [rank A4, A40].

### 2.5 Produto e mix

- **Painéis oficiais primeiro:** Tendências por categoria e Concorrência (até 50 anúncios, números aproximados, só logado) [mix A1, A2]. Sem login, só a contagem de anúncios é pública [mix §12.3, R2-MIX-3].
- **Triangular a demanda** com visitas, avaliações novas e idade do anúncio, sem somar ferramentas [mix §3.1]. As ferramentas N5 perderam base pública com o fechamento da API [mix A18].
- **Critérios de entrada** (prática) [mix §3.2]:
  - visitas;
  - margem depois de tarifa e envio;
  - quem domina o catálogo e se o preço do vencedor cobre o *break-even*;
  - presença do ML em 1P, agora com base N2 [mix §12.3, R2-MIX-8].

  Um terço da 1ª página é pago [mix §12.3, R2-MIX-6].
- **Ciladas:** tarifa mais envio acima de 30% do preço; vencedor do catálogo abaixo do seu *break-even*; demanda nas mãos de poucos [mix A21].
- **Escada de kits:** 1, 2, 3, 5, 10 e 20 unidades. Kit de unidades iguais não pode ser kit virtual [mix A26].
- **Racionalização** (prática) [mix §3.5]: ABC por lucro; compra de 90 dias igual a 3 vezes a venda de 30, ajustada; margem abaixo de 10% trava a compra.
- **Papéis no portfólio:** estrela vai ao Full com ROAS alto; novo fica fora do Full com ROAS baixo; kits misturam rotações [mix §7].
- **Divergência sem resolução:** cauda longa contra poucos SKUs profundos [mix §3.5].

### 2.6 Reputação e atendimento

- **Rotina diária da página de reputação**, com alerta interno a 50% do limite (prática, fonte única com tela) [rep A34].
- **Atrasar em vez de cancelar:** o limite de envios com problema é de 5 a 7 vezes o de canceladas (10% contra 1,5% em 60 d; 13% contra 2,5% em 365 d). A lógica vem dos limites oficiais, sem texto que a recomende [rep A35].
- **Folga real no corte de 101 vendas:** 2 reclamações mantêm o verde, e a 3ª leva ao amarelo (cálculo com limite oficial) [rep §4].
- **Resolver em até 48 h, antes da mediação** [rep A11].
- **Corrigir a causa no anúncio** (foto fiel, medidas, motivos de devolução) e operar sem falha (estoque sincronizado, despacho no mesmo dia, perguntas em cerca de 12 h) [rep §3].
- **Programas como colchão:** Decola e Protegida mascaram a cor sem mudá-la; a Protegida vem sendo oferecida a contas verdes [rep A21, A22; R2-SIN-8].
- **Limites:** não há ferramenta oficial para pedir avaliação [rep A29].

### 2.7 Alimentos e marca própria

- **Linha completa:** grão, moído, cápsula e drip; 250 g, 500 g e 1 kg [obs 3; alim §5.8].
- **Full como padrão.** No Supermercado, a restrição vale só para a lista de produtos de autorizados [alim A3].
- **Preço em camadas:** preço riscado, Pix (de 8% a 53% OFF), preço por kg e desconto por quantidade [obs 4–5]. O desconto por quantidade oficial não vale para itens vendidos por kg [mix A8].
- **Informação de uso para reduzir reclamação:** escala de intensidade e explicação da válvula [alim §3.1].
- **Registro de marca e BPP** [alim A11, A12]. Grupos com várias marcas operam várias lojas oficiais numa só conta de vendedor (observação de 15/10) [R2-EVC-23 a 25].
- **Rentabilidade por pedido e equipe por canal × categoria** (prática) [alim §5.9].

### 2.8 Cases grandes

Todos os números de case são autodeclarados e ficam como [PRÁTICA] C. Uma busca dirigida não achou case de vendedor do ML com período, base e medição de terceiro [cases A9; R2-EVC-17 a 22].

- **Pontos em comum** [cases §3.2, A7]: de 95% a 97% das vendas pelo Full (o ML não divulga o número do Brasil), operação perto dos CDs de SP, cadastro disparado pela nota de entrada, margem conciliada por pedido, matriz canal × categoria e times enxutos.
- **Erros documentados:** concentração de 80% do faturamento em um item, sair do nicho, 7.000 SKUs e fornecedor que não acompanha a demanda [cases A14–A17].
- **Reação à regra de preço:** preço único entre canais ou linhas exclusivas por canal [cases A4].
- **Revenda que vira marca:** 3 de 11 cases migraram por guerra de preço no catálogo [cases A18].
- **Apoio da plataforma:** agências certificadas (Mercado Ads Partners, em 3 níveis) e assessoria do ML que pode operar a conta [R2-WEB-25; webinars §11].

---

## 3. Benchmarks

São faixas, não médias. O ML não publica benchmark por categoria. "Sem método" quer dizer que a fonte não declara amostra, período ou definição.

| Indicador | Faixa | Amostra / método | Tipo, confiança | Fonte |
|---|---|---|---|---|
| ACOS máximo | Igual à CM1% | Método aritmético | [PRÁTICA] B | [ads A22] |
| ROAS objetivo permitido | 1x a 35x | Regra | [OFICIAL] | [ads A2] |
| ROAS de partida | Prática 8–15 (2–5 em lançamento); social 15–25; fala oficial 10 (casos de 3 a 40) ou 5 | **Sem método** | C | [ads A24; soc S03–S04] |
| TACOS-alvo | 1,5–6% declarado; 0,6–5,8% em telas | Telas de praticantes | [PRÁTICA/CASE] C | [ads A28; soc S06] |
| Vendas vindas de Ads | 27–81% por conta | **Sem método** | C | [ads A29] |
| ACOS "bom" por categoria | 5–25%; blog: 5% excelente, 15% bom, 50% preocupante | **Sem método** | C | [ads A37; R2-DAD-28] |
| Amazon EUA, Food & Grocery | ACOS 21% (35% em contas grandes) | Compilação; só ordem de grandeza, outra plataforma | C | [ads A38] |
| Posição e Ads (ML) | Com Ads, 70% das impressões no top 8. Orgânico: 4% nas 2 primeiras posições, contra 27% com Ads. 40% das vendas de Ads fora da busca | DADO do ML, **sem método** | baixa-média | [ads A20; R2-WEB-27, 28] |
| Seguidores | Compram 60% mais e com frequência 50% maior | DADO do ML, **sem método** | baixa | [webinars §10] |
| Conversão | +1,1 p.p. a/a no Brasil (2T26). A absoluta não é pública. Prática: "boa" de 3–6% (R$19–79), 1,5–5% (R$79–250) e abaixo de 1% acima de R$250 | N2 por transcrição de terceiro; prática **sem método** | N2 / C | [rank A39; R2-BA-28] |
| Conteúdo e conversão | De 15% para 43% em 6 meses | 1 SKU, sem controle | [CASE] C | [R2-DAD-20] |
| Clipe | +10–15% (clipe na 1ª posição); 38% × 27% de conversão para quem assiste; 3x visitas e 2x vendas | Declarado pelo ML, **sem amostra** | baixa | [rank A25, A26] |
| Margem-alvo | Revenda 15–20%; importado acima de 30%; fabricante 25–35% | **Sem método** | [PRÁTICA] C | [pre A25; soc S10] |
| Margem de grandes | MC de cerca de 28% e lucro líquido de cerca de 10% (moda com fábrica) | Autodeclarado | C | [cases A12] |
| Peso da plataforma no café (fora do Super, Clássico) | 250 g a R$35: envio R$6,95 + tarifa R$4,90 = cerca de 34%. 1 kg a R$85: R$14,45 + R$11,90 = cerca de 31%. No Premium (19%): cerca de 39% e 36% | Cálculo com tabela oficial, sem imposto, Ads nem embalagem | Cálculo | [alim §5.7, §12.2] |
| Café no Full Super "selecionado" | Envio de R$1,60 no item de R$35, cerca de 5% (a tarifa do Super não foi lida) | Cálculo com tabela oficial | Cálculo | [alim §5.7; alim A7] |
| Cobertura no Full | 4–8 semanas (fala oficial); envios de 15–30 dias (prática) | **Sem método** | B/C | [log A14, A30] |
| Giro para ir ao Full | Cerca de 3 un/dia ou cerca de 2 meses de curva A | **Sem método** | C | [soc S14; log A28] |
| Ruptura e posição | Um dia sem estoque tira do top 30 46% dos itens do top 5 (mais de 64% em café); 37,9% voltam no 1º dia e 59% no 2º | Lett, **amostra não declarada**, sem nome de marketplace | N4 C | [R2-DAD-17] |
| Ruptura no e-commerce | 30,5% (jan–set/2024); 30% na Black Friday; estoque dura 5,85 dias em Alimentos | Lett EQI, cerca de 700 a 750 mil páginas | N4 B/C | [R2-DAD-16, 18] |
| Patrocinado na busca | 8 de 24 (33%) em 6 termos; slots 1–4 e 13–16 | OBS: 6 termos × 24, sessão logada, um horário, sem CEP | [OBS] alta para a sessão | [R2-OBS-2] |
| Full no topo | Café: 83–92% Full Super. Fora de café: FULL 38–88%, frete grátis 92–100%, loja oficial 29–67% (café: 0–8%) | Idem | [OBS] | [R2-OBS-5, 6] |
| Full no topo (14/10) | 26/40, 21/30 e 22/25 com FULL em buscas de café | OBS, CEP em MG, pago e orgânico misturados | [OBS] | [obs 1] |
| Preço por kg de café | Supermercado R$32–84; especial de marca R$90–160; microlote acima de R$200 | OBS de 13 páginas | [OBS] | [obs 4] |
| Galeria | 6–9 fotos nos líderes de café; "média de 8" em algumas categorias | OBS; prática | [OBS]/C | [obs 9; rank §4] |
| Concentração | 63–74% de vendedores Platinum em categorias "saturadas" | Nubimetrics, **sem método** | N5 C | [mix A24] |
| Oferta no café | A&B cerca de 1,5 mi de anúncios; Café cerca de 39–40 mil; Cápsulas cerca de 16–17 mil | API pública (contagem, não demanda) | [OFICIAL] A | [R2-DAD-25] |
| Alimentos no online | 1,4% do valor de Alimentos vendido online (H&B: 8,3%). O online chega a 45,4% dos lares, mas responde por 2% das ocasiões | NIQ (transações mais pesquisa); Worldpanel (painéis de mais de 10 mil e 11.300 lares) | N4 B | [R2-DAD-02, 12, 13] |
| Tamanho e share | E-commerce de R$351,4 bi em 2024 (NIQ). ML com cerca de 42% (UBS); tamanho de R$235,5 bi a R$450 bi conforme o método | NIQ com método; UBS e IRTT **sem método** | B / C | [R2-DAD-01, 06, 09] |
| Devolução saudável | Cerca de 2% em eletrônicos; o ML não publica | **Sem método** | C | [rep A37] |
| Reclamações de alimentos | 6 de 63 registros (27/09–15/10/2026), dominadas por validade | Reclame Aqui, amostra pequena | N8 | [R2-SIN-19 a 21] |
| Efeito do prazo (externo) | Cerca de +1,45% nas vendas online por dia útil a menos | Quase-experimento, varejo de vestuário nos EUA | N4 alta no contexto | [R2-EVC-10] |
| Efeito do frete (externo) | Frete grátis incondicional: +2,2% ou mais de conversão contra frete com mínimo | Experimento aleatório | N4 | [R2-EVC-13] |

---

## 4. Divergências que restam e como medir

### 4.1 Em aberto

| # | Divergência | Lados | Estado | Como medir |
|---|---|---|---|---|
| 1 | Requisitos do Product Ads | Texto sem data (com "anúncio ativo no catálogo" e dispensa pelo Decola) × 3 falas de 2026 (com 15 dias de conta e sem fatura vencida) | ABERTA [ads A6; rep A16] | Elegibilidade numa conta nova; fonte escrita datada |
| 2 | Atribuição do Ads | 14 dias (texto) × 15 dias (fala de maio) | PARCIAL; o texto pesa mais [ads A10] | Painel do Ads; vendas atribuídas no 15º dia |
| 3 | Fórmula do leilão do Product Ads | Ad Score × CPC (fala de maio) × três variáveis (fala de set) × ROAS + relevância (texto); "segundo preço" oral | PARCIAL [ads A4] | Página escrita; transcrição de nova live oficial |
| 4 | Ads eleva o orgânico? | Fala do ML: "traz posicionamento", +21% de cliques e +39% de vendas (atribuição) × literatura externa (substituição, exceto em produto novo ou ranking por volume) | ABERTA [rank A42] | *Holdout* ou pausa por SKU pareado; geo-teste; vendas sem publicidade |
| 5 | Pago e orgânico juntos | O mesmo produto aparece até 4 vezes no top 24 [R2-OBS-4] | Indício, não medida | Pausa controlada com leitura de posição orgânica |
| 6 | Frete grátis fora da loja Full Super | R$79 (16449) × R$19 (40538) | Não resolvida [log §12.2] | Para custo, vale a 40538; checar o simulador logado |
| 7 | Valor do TH (custo fixo) | Não publicado; candidatos: R$19, R$79 | ABERTA [R2-BA aberto 2] | FAQ de pricing; faturas por faixa |
| 8 | Nota antiga de custo fixo no ar | "<R$12,50 = 50%" (sem data) × developers de 03/09/2026 | Resolvida a favor da developers, com ressalva de leitor único [mix §12.2] | Fatura de venda no Flex e no Full abaixo de R$79 |
| 9 | Rótulo de peso do Full Super | Mesmos valores rotulados "até 1 kg" (rodada 2) e "até 0,3 kg" (nota de preço) | ABERTA [pre §12.5] | Reler a ajuda/49972 |
| 10 | Ids e página de origem | Estoque antigo: 15731 × 15373. Armazenagem do Super: 21793 × 24253 | Mesmo conteúdo; divergência de citação [log §12.1] | Conferir redirect |
| 11 | Bonificação do VOLUME | Tabela de 2026 com bonificação × doc de 2025 sem | ABERTA [pre A18] | Reler a doc de Volume; campo `meli_percentage` num item |
| 12 | Isenção de 180 dias para estrelas | Fala oficial × nenhuma página escrita | PARCIAL [log A5; mix A12] | Fatura de estoque antigo de um SKU estrela |
| 13 | Cobertura máxima no Full | "30–45 dias" (vídeo) × "não ultrapassem 2 meses" (ajuda) | ABERTA [log A15] | Índice do Full e custo por SKU |
| 14 | Ganho de vendas com Full | "Até 2x" e "70% dos anúncios +150%" (ML) × "até 5x" (praticante) | ABERTA, sem método [log A17] | Antes e depois com SKUs pareados fora do Full |
| 15 | Editar anúncio com vendas | API bloqueia título × fala diz que é possível e que o anúncio vira "novo" | PARCIAL [rank A20] | Série de posição antes e depois de edição controlada |
| 16 | Logo e conversão de clipe | Logo "na tela e no tempo" × "na tela ou no tempo"; conversão de 38% × 27% | Divergência entre falas [rank A25, A27] | Cumprir as duas condições; número sem método |
| 17 | Benefício × Protegida | Mesmo regulamento (link e id) sem frase oficial; a developers exclui o verde, a 29528 aceita | ABERTA [rep §12.1] | Painel logado `/reputacao/beneficio_reputacao` |
| 18 | Complemento da experiência | "200 vendas" (nota) × "200 em 60 dias" (vídeo); 180 dias por leitura cruzada | Vale a nota [rep A20] | Comparar a tela com as vendas da janela |
| 19 | Punição por preço externo | Só imprensa (out/2025) × comparação externa oficial | PARCIAL [cases A3] | Avisos na Central; elegibilidade a cofinanciadas |
| 20 | Efeito da medalha | Oficial: mais visibilidade × praticante: nenhum efeito | ABERTA [rep A38] | Impressões antes e depois da troca de medalha |
| 21 | A descrição indexa? | "Não indexa" × "cole palavras-chave no fim" | Sem fonte [soc S20–S21] | Buscar termo presente só na descrição |
| 22 | Preço de entrada | Começar baixo × começar alto e descer | Sem teste [pre D1; mix §3.2] | SKUs pareados |
| 23 | Lista restrita do Supermercado | Restrição a autorizados × entrada automática dos demais | Escopo conciliado; lista não pública [alim A3] | Fluxo de envio ao Full no painel |
| 24 | Incoerências da ajuda/16645 | Faixas de retirada fora de ordem | Leitor único [log §12.3] | Reler em outro dia |
| 25 | Sinais do patrocinado | "45 de 45" no relatório × 31 de 31 com os três sinais no TSV | Vale 31 de 31 [soc, Limites] | Repetir a coleta checando os três sinais |
| 26 | Datas sem fonte | Ano de 10/09 (inferido); 20/05 dos extragrandes; metadado "15 de outubro" da 44922 | Inferência [rep A2; log A9] | Novidades da Central (exige login) |

### 4.2 Resolvidas desde 14/10

- **Desconto por reputação:** vale 50% / 40% / 0% [rep A15].
- **Corte de reputação:** 101 vendas; o 68 é erro [rep A2].
- **Decola:** 365 dias [rep A21].
- **Experiência de compra:** janela de 60 dias ou do último ano [rank A9].
- **Custo fixo:** regra de 02/03/2026 [mix A37].
- **Estoque antigo em alimentos:** 2 meses no Supermercado; R$1/12/28 é a tabela geral [cases A36].
- **Desconto de frete no Full:** tabela única para Full, Coleta e Agência [rep A27].
- **Limites de peso:** 25 kg é a entrada, 18 kg é o tamanho XG de armazenagem, 20 kg / 80 cm / 125 L é a lista de extragrandes [log §12.2].
- **Classe do INPI:** o ML não exige; o café é classe 30 [alim A27].
- **Price matching:** 10 dias e duas modalidades [pre A19].
- **01/09/2026:** não é prazo do café [alim A16].
- **"60 dias antes da Black Friday":** não é lei [pre §12.1].

---

## 5. Indústria/marca própria × revenda

| Alavanca | Favorece | Por quê | Fonte |
|---|---|---|---|
| Catálogo e buy box | Revenda eficiente | O algoritmo escolhe por preço total, Full, parcelas e reputação, não pela dona da marca. Num catálogo de café de 1 kg havia 72 ofertas e quem ganhava era um supermercado | [rank A4; obs 2] |
| Avaliações e "vendidos" | Marca | Pertencem ao produto de catálogo; a revenda usa, mas não controla | [rep A40] |
| Clipe no catálogo | Marca | O clipe da marca é exibido primeiro, mesmo sem vencer (fala) | [rank A28] |
| Loja oficial, Brand Ads, Minha Página | Marca | Exigem registro no INPI; o Brand Ads é o único formato com palavra-chave | [alim A11; ads A8] |
| BPP | Marca | Gratuito; cobre marca, desenho, autoria e patente | [alim A12] |
| GTIN e "selecionados" do Full Super | Marca com EAN e catálogo | O GTIN pontua na qualidade; o benefício dos selecionados vale automaticamente para anúncio de catálogo (critério não publicado) | [rank A13; alim A7] |
| Desenho do produto para o Full | Marca | Só quem fabrica ajusta peso e medida à classe mais barata | [log §7] |
| Margem para ROAS de lançamento | Marca | Margem bruta maior aguenta ROAS baixo na fase de teste | [ads §3.1] |
| Preço de lista e price matching | Contra a marca multicanal | O ML lê preços externos e gera ofertas de equiparação; não há política de preço mínimo para a marca | [pre §5, §7; pre A24] |
| 1P do ML | Contra as duas onde falta seleção ou preço | 1P abaixo de 10% do GMV, preenche lacunas; "Basics" sem fonte | [R2-BA-18, 19; alim A28] |
| Escala de compra e subsídio do fornecedor | Revenda | Compra com prazo e liquidação paga pelo fornecedor | [cases §7] |
| Peneira e cauda longa | Revenda e importação | Muitos SKUs e concentração nos vencedores | [ads §7; mix §3.5] |
| Estoque compartilhado | Revenda do mesmo EAN, fora de alimentos | Unidades iguais geridas juntas; exclui alimentos e qualquer item com validade | [log A22] |
| Anúncio separado por envio | Os dois | Permite separar Full de Flex ou Coleta sem infringir a regra de duplicados | [rank A22] |

**Específico de revenda e importação**
- Disputa de buy box em catálogo alheio, sem controle de título, foto ou avaliação [pre §7; obs].
- Margem-piso alta e calendário de importação [mix §7].
- Teste de lote e risco de fornecedor [rep §3; cases A17].
- O dropshipping é incompatível com o Full e piora o tempo de disponibilidade, que pontua na qualidade [rank §7; rank A13].

**Específico de indústria e marca própria**
- Defender o próprio catálogo nas mesmas variáveis da buy box [rank §5].
- Conflito com a tabela do canal físico [cases §5].
- Linhas exclusivas por canal [cases A4].
- Regularização sanitária e rótulo próprios. No café, o formulário do comunicado pede o detentor da marca quando ele difere do detentor da regularização [R2-REG-13].
- Grupos multimarca concentram várias lojas oficiais numa conta, com a mesma reputação (inferência) [R2-EVC-23 a 25].

---

## 6. Alimentos e café

### 6.1 Regras da plataforma

Os valores estão na §1. O que importa para alimentos:
- **O Full decide a viabilidade.** Ele exige validade acima de 90 dias, rótulo legível em português e registro na Anvisa ou no MAPA. Recusa refrigerados, validade próxima e pack sem EAN. Fora do Full não há validade mínima publicada [alim A1, A2; log A8, A38].
- **Supermercado.** A restrição a autorizados vale para uma lista não pública de produtos. Os demais entram automaticamente quando estão no Full (inferência média) [alim A3; R2-FS-1 a 5].
- **Full Super.** O envio dos "selecionados" custa R$1,60, contra R$6,95 do envio comum de 0,3–0,5 kg na mesma faixa [alim A6–A8].
- **Validade vira custo.** O estoque antigo começa aos 2 meses no Supermercado [alim A4]. Não há economia de volume no Supermercado [alim A9], e o desconto por quantidade não vale para itens por kg [mix A8].
- **Tarifa.** A redução de 3 ou 5 p.p. entre R$150 e R$700 deixa kits e packs nessa faixa mais leves em tarifa [R2-BA-4].
- **Exclusões.** O estoque compartilhado exclui alimentos [alim A32]. A API de reclamações tem o grupo `expiring_food` [rep A33]. Há sinal N8 de restrição nova a bebidas alcoólicas no Full [alim A33].
- **Recorrência.** O MELI+ não cobre Supermercado. Não existe assinatura de produto; há botão de recompra, sem dado de uso [cases A31; alim §12.4 Q4].

### 6.2 Regulatório (lido na fonte)

- **Via sanitária do café** [R2-REG-11, 12; alim A15]:
  - o café está no Anexo III, item 5, da IN 281/2024;
  - a obrigação é comunicar o início de fabricação ou importação à vigilância sanitária local; não é registro nem notificação;
  - pela RDC 843/2024, art. 26, o produto pode ir ao mercado depois do protocolo; o comunicado não aprova o produto e vale por prazo indeterminado;
  - a autoridade pode inspecionar a critério dela (art. 27).
- **O prazo de 01/09/2026 não é do café.** Ele vale para produtos do Anexo I e para notificar suplementos e alimentos para controle de peso [R2-REG-14; alim A16].
- **Alegação funcional:** pela leitura do analista, um café com alegação funcional cairia na notificação (Anexo II), sem confirmação da Anvisa [R2-REG-17].
- **Marca terceirizada:** o formulário do Anexo XI pede o detentor da marca quando ele é diferente do detentor da regularização [R2-REG-13].
- **Rótulo do café, Portaria SDA 570/2022, art. 41** (vigente desde 01/01/2023) [R2-REG-15 a 17; alim A14]. Campos obrigatórios:
  - grupo;
  - "fora de tipo", quando for o caso;
  - espécie ("100%" ou "predominantemente");
  - "café" seguido da marca;
  - lote;
  - CNPJ ou CPF e endereço;
  - ponto de torra.

  A moagem é opcional. O art. 47 veda função terapêutica ou funcional não autorizada. O art. 48 dispensa o Documento de Classificação na venda direta por e-commerce, desde que o produto esteja conforme. "Arábica e Conilon lado a lado" é interpretação da FAQ do MAPA, não texto da portaria.
- **Rótulo × anúncio:** não há norma sanitária específica para o anúncio online. A RDC 727/2022 define rotulagem como o que está na embalagem [R2-REG-19 a 24]. O dever vem de quatro textos:
  - CDC, art. 31: composição, validade, origem e riscos, em português;
  - Decreto 7.962/2013, art. 2º: CNPJ, endereço e características essenciais, em destaque;
  - Lei 10.962/2004, art. 2º, III: preço à vista junto à imagem, em fonte de no mínimo 12;
  - Decreto-Lei 986/1969, art. 23: as regras de rotulagem valem para a propaganda em qualquer veículo.

  A revisão de rotulagem aberta em 2025 não trata de comércio eletrônico.
- **INPI** [R2-REG-31 a 34; alim A26, A27]:
  - pela NCL 13-2026, o café é classe 30, e na classe 35 "a venda de produtos não é considerada um serviço";
  - o ML pede registro vigente e não cita classe;
  - a Portaria 66/2026 criou trâmite prioritário para quem precisa da marca registrada para vender em plataforma (vigor em 01/05/2026), com 1.500 pedidos por quadrimestre e no máximo 10 por requerente;
  - prazo e taxa não estão nas portarias.
- **Fiscalização** [R2-REG-1 a 10; alim A13]:
  - a Anvisa inspecionou o CD de Cajamar em 18/03/2026, com foco em itens do Full, e mandou retirar anúncios na hora;
  - a "rotulagem em idioma estrangeiro" estava ligada a produtos de saúde;
  - o 0,34% é declaração do ML à imprensa;
  - a Anvisa age sobre a propaganda com alegação de saúde (RE 1.045, 521 e 200/2026);
  - Senacon e Anvisa preparam acordo sobre suplementos em marketplaces;
  - o alerta de risco do MAPA tem 1 lote de café em 2026, sem marketplace como varejista.

### 6.3 O que a observação mostra em café

- **Busca de 15/10** [R2-OBS-5, 6]:
  - de 83% a 92% do top 24 são cards Full Super, sem nota, vendidos nem vendedor;
  - só de 2 a 4 dos 24 cards mostram nota;
  - a loja oficial aparece em 0% a 8%;
  - há um carrossel "Adicione mais de FULL SUPER";
  - a prova social fica na página do produto, não no card.
- **Líderes, 14/10** [obs 1–10]:
  - linha completa em várias posições;
  - preço por kg visível;
  - desconto por quantidade dentro do anúncio;
  - MercadoLíder Platinum e lojas com dezenas de milhares de seguidores;
  - título do líder em grão genérico e rico em palavra-chave;
  - buy box de marcas grandes frequentemente com revendedor;
  - top 20 de Alimentos e Bebidas só com marcas nacionais muito conhecidas.
- **Especial sem Full:** aparece no topo com poucas vendas, salvo exceções com volume [obs 1].

### 6.4 Demanda, recorrência e queixas

- **Teto do canal:** 1,4% do valor de Alimentos é vendido online. O online chega a 45,4% dos lares, mas responde por 2% das ocasiões; o desafio declarado é converter experimentação em recorrência [R2-DAD-02, 12, 13].
- **Café** [R2-DAD-14]: consumo −2,31% em 2025; preço da cápsula −16,8% e do gourmet +20,1% (ABIC, sem recorte por canal).
- **Supermercado do ML**, segundo executiva à imprensa (2025, pode estar superada): sortimento +74% em 6 meses e 1 em cada 4 compradores novo na categoria [R2-DAD-15].
- **Proxies de recompra** (N2): itens por comprador +19% e +10 p.p. de usuários em 3 ou mais categorias. Não há taxa de recompra por categoria [R2-DAD-11].
- **Queixas** (N8) [R2-SIN-19 a 21]:
  - padrões: validade curta ou vencida, data adulterada, avaria e embalagem inadequada;
  - aparece a exigência de devolver o item vencido para receber o estorno;
  - o atraso não aparece ligado a alimento;
  - a embalagem e a informação de uso reduzem queixas de expectativa [alim A31; rep §5].

---

## 7. Evidência causal

### 7.1 O que existe na literatura (nenhum estudo é do ML)

| Tema | Achado | Fonte | Transferência ao ML |
|---|---|---|---|
| Ads em termo de marca | No eBay, desligar anúncios de marca manteve 99,5% dos cliques pelo orgânico; anúncio genérico com ROI negativo | R2-EVC-1 | Média: o Product Ads não expõe termo de busca |
| *Holdout* de Ads | Com 3% sem anúncios, o anúncio desvia venda do orgânico e reduz o volume total, mas dá lucro à plataforma | R2-EVC-2 | Média |
| Heterogeneidade | Flipkart: o anúncio converte pior que o orgânico deslocado em eletrônicos e melhor em moda | R2-EVC-3 | Média |
| Produto novo | JD.com usa a propensão a anunciar como sinal no início de vida do produto; app store: desligar anúncios cortou de 20% a 30% dos downloads orgânicos quando o ranking é movido por volume | R2-EVC-4, 5 | Mecanismo plausível, não testado |
| Carga de anúncios | Mais vagas pagas elevam a receita da plataforma e reduzem conversões totais | R2-EVC-6 | Coerente com 33% do topo pago |
| Posição | Expedia: a posição muda o que é examinado, não a compra condicionada | R2-EVC-7 | Média |
| Buy box | eBay: destacar a melhor oferta em bem homogêneo pode ser pró-competitivo | R2-EVC-8 | Lógica do catálogo |
| Reputação no ranking | eBay: promover vendedores de maior qualidade elevou em 0,3 p.p. a volta do comprador | R2-EVC-9 | Explica o peso da experiência |
| Prazo | Cerca de +1,45% nas vendas por dia útil a menos | R2-EVC-10 | Ordem de grandeza para o Full |
| Frete | Frete grátis incondicional: +2,2% ou mais de conversão; frete grátis acima de um mínimo vende mais, mas gera mais devoluções | R2-EVC-13, 14 | Coerente com a faixa de R$19–79 |

### 7.2 O que o ML afirma sem método

São números de webinars oficiais, sem base nem controle [webinars aberto 9; rank A25, A26]:
- 38% contra 27% de conversão com clipe; +10% a 15% com o clipe na 1ª posição; 3x visitas e 2x vendas;
- vencer o catálogo dá 4% das posições de busca, contra 53% vencendo com Ads;
- 4% contra 27% das impressões nas 2 primeiras posições;
- 40% das vendas de Ads fora da busca;
- +21% de cliques e +39% de vendas ao ligar Ads;
- +70% com agências Partners; "até 2x" e "+150%" com o Full;
- seguidores compram 60% mais.

### 7.3 O que o ML não publica

- Nenhum experimento de busca, Ads ou Full no blog técnico, e nenhum paper com experimento aleatório no ML [R2-EVC-16].
- Fórmula e pesos do ranqueamento [rank §12.4 Q1].
- Ads/GMV, penetração do Full no Brasil e conversão absoluta [R2-BA-15, 17, 28].
- Página de cases do Mercado Ads: o "9x" é declarado com base em dados internos [R2-EVC-22].
- Tempo para ranquear anúncio novo ou para recuperar posição depois de ruptura [rank §12.4 Q8; log §12.4 Q7].

### 7.4 Atribuição que parecia causa

- **R$19 de frete grátis:** antes e depois. O México teve os mesmos +42% e +34% no 3T25 [cases A5].
- **TACOS e "score de TACOS":** sem fonte oficial [ads A33].
- **Full no topo de café:** é observação, não causa. O orgânico é mais Full que o pago (16/16 contra 4/8), o que sugere que o slot pago abre espaço a quem não está no Full [soc, Observação com protocolo].

### 7.5 Desenhos de medição citados nas notas

Pausa ou *holdout* de Ads por SKU pareado [ads §12.4 Q5]; antes e depois do Full com controle [log A17]; série de posição após edição ou ruptura [rank A20; log A13]; separação de subsídio pelos campos `meli_percentage` e `seller_percentage` [pre §12.4 Q6]; observação repetida em outro horário, deslogada e com CEP [R2-OBS aberto].

---

## 8. Perguntas abertas para a fase de estratégia

1. **Supermercado:** um item de café está na lista restrita a autorizados? Isso só se vê no fluxo de envio ao Full, no painel [alim A3; R2-FS aberto 2].
2. **Full Super:** qual o critério e a lista dos "selecionados" (PDF não lido)? Qual o rótulo de peso correto da tabela? [alim A7; pre §12.5]
3. **Tarifas não lidas:** qual a tarifa da seção Supermercado e o percentual-base de Cápsulas? [cases A29; R2-BA aberto 3]
4. **Limite de frete grátis:** qual o valor do TH, e o frete grátis fora da loja Full Super é de R$19 ou R$79? [R2-BA aberto 2]
5. **Product Ads:** quais os requisitos (texto × fala) e a janela de atribuição? Quem recebe a venda quando o clique pago leva a um catálogo ganho por outro? [ads A6, A10; R2-WEB-18]
6. **Incrementalidade de Ads:** qual o efeito incremental, inclusive em termos da própria marca, que o Product Ads não expõe? Quanto da exposição paga duplica o orgânico? [ads §12.4 Q5, Q6; R2-OBS-4]
7. **Pesos do ranking:** quanto o Full pesa contra o preço? Quanto tempo leva para recuperar a posição depois de uma ruptura no ML? [log §12.4 Q3, Q7]
8. **Anúncio novo:** em quanto tempo ganha posição orgânica? Há só referências de Ads [rank §12.4 Q8].
9. **Preço externo:** existe regra formal de paridade? Quais canais são monitorados? Qual o efeito no pacote de abril/2026 e nas cofinanciadas? [cases A3; pre §12.4 Q2]
10. **Benchmarks de alimentos no ML:** quais as faixas de conversão, ACOS e TACOS, devolução e recompra? [alim §12.4; ads §12.4 Q7]
11. **Painel Concorrência aplicado a café:** qual o share por vendedor e o uso de Ads, Full e promoções pelos líderes? Exige login [cases §12.4 Q2].
12. **Devolução de alimento:** qual a regra, o destino da unidade aberta e o custo do arrependimento em perecível? [rep §5; R2-SIN-21]
13. **Recorrência:** que mecanismo existe além do botão de recompra e dos seguidores, se o MELI+ exclui Supermercado? [alim §12.4 Q4]
14. **Observação:** como mudam os números com 2º horário, sessão deslogada, CEP explícito e série temporal? [R2-OBS aberto]
15. **Balanço do 3T26** (fim de outubro): o que traz sobre o pacote de preço, o MELI+, o 1P e o Full? [R2-BA aberto 7]
16. **Regulatório:** um café com alegação funcional muda de via sanitária? O anúncio precisa reproduzir o rótulo? O que o "Minhas Marcas" aceita na prática? Qual o prazo e a taxa do trâmite prioritário do INPI? [regulatorio, Aberto 6–9]
17. **Contas de grupos multimarca:** quem opera cada conta, e o ML vende essas marcas em 1P? [alim §12.4 Q9]
18. **Sortimento:** quantos SKUs e formatos ocupam mais de uma posição sem diluir o giro no Full e o índice? [mix §9; log A4]
19. **Calendário:** qual o calendário promocional de 2026 e os prazos de adesão da Black Friday (27/11)? [pre §12.4 Q8]
20. **Outras plataformas:** Shopee e Amazon ficam para as frentes próprias [ads A39–A41; alim A17, A18].

---

## 9. Índice de arquivos

Raiz: `pesquisa-marketplaces/`.

**Método e controle**
- `metodo/protocolo.md`: regras, hierarquia de fontes, tipos, sinais de conteúdo fraco e perguntas por frente.
- `metodo/estado-da-arte.md`: base metodológica do protocolo.
- `LACUNAS.md`: lacunas e reconciliações (§1.9) usadas na rodada 2.
- `LEIA-ME.md` e `INDICE-YOUTUBE.md`.

**Notas de frente (`mercadolivre/<frente>/notas.md`; o estado final está na §12)**
- `ads/`, `preco-promocao/`, `logistica-estoque/`, `ranqueamento-anuncio/`, `produto-mix/`, `reputacao-atendimento/`, `alimentos-marca-propria/`, `cases-grandes/`.

**Rodada 2 (`mercadolivre/rodada2/`)**
- `regulatorio.md`: Anvisa, IN 281, RDC 843, Portaria 570, INPI, CDC e "de/por" (R2-REG).
- `balancos-api.md`: tarifas, balanços, MELI+ e restrições de API (R2-BA).
- `webinars.md`: 12 vídeos oficiais com minuto (R2-WEB).
- `dados-mercado.md`: NIQ, Worldpanel, ABIC, Lett e Nubimetrics (R2-DAD).
- `evidencias-cases.md`: experimentos, cases e lojas oficiais (R2-EVC).
- `sinais-recentes.md`: mudanças dos últimos 60 dias e Reclame Aqui (R2-SIN).
- `nav-full-supermercado.md`: Full, Supermercado e estoque (R2-FS).
- `nav-preco-reputacao.md`: tarifas, promoções, reputação e experiência (R2-PR).
- `nav-observacao.md`, `nav-observacao.tsv` e `nav-observacao-prints/`: busca orgânica × patrocinada (R2-OBS).

**Verificação**
- `verificacao/resultado-mercadolivre.tsv`: 46 releituras oficiais (seções 10 e 11).
- `verificacao/pendentes-mercadolivre.tsv`.

**Social e observação**
- `mercadolivre/social/notas.md`, `posts.tsv`, `posts.txt`, `tiktok.txt` e `transcricoes/` (23).
- `mercadolivre/observacao/lideres.md` e `lideres.tsv` (14/10/2026).

**Coleta de vídeo**
- `mercadolivre/videos.tsv` (313), `selecionados.tsv` (91), `consultas.tsv` e `transcricoes/` (87).
