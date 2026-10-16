# TikTok Shop Brasil: mapa de conhecimento consolidado

Versão de 2026-10-15. É uma pesquisa neutra sobre como a plataforma funciona e como os melhores operam nela. Não parte da situação de nenhuma empresa e não traz recomendação para nenhuma.

**Para que serve.** É o ponto de partida de quem vai desenhar estratégia e agentes. Cada afirmação aponta para a nota de origem, onde estão a URL, o id do vídeo e o raciocínio. Quando o corpo de uma nota e a verificação (seções 10 e 11 de cada nota) divergem, **vale o que a fonte oficial diz** e esta versão já traz o valor corrigido.

---

## Cabeçalho

### Fontes por camada

| Camada | O que entrou | Contagem |
|---|---|---|
| Notas de frente | 16 notas (ads, preço-promoção, logística, ranqueamento-vitrine, produto-mix, reputação, alimentos, cases, conteúdo-vídeo, live, afiliados, onboarding, conta de marca, dados de mercado, ferramentas, regulatório), cada uma com 9 seções, tabela de afirmações e verificação em duas rodadas | cerca de 143 mil palavras na contagem bruta (wc); cerca de 590 afirmações |
| Oficial BR (N1) | TikTok Shop Academy BR (`seller-br.tiktok.com/university/essay?knowledge_id=<kid>`), Newsroom BR, canais oficiais @tiktokshopcreators.br e @sellwithtiktokshop_br, blog TikTok Ads pt-BR | cerca de 90 páginas distintas lidas |
| Oficial global e EUA | Central de ajuda do TikTok Ads (não diz país), Seller University EUA (via ppc.land), webinar com a chefe de alimentos do TikTok Shop EUA (tGotPuBPS08), guia F&B (PDF, EUA e Sudeste Asiático) | cerca de 30 páginas |
| Lei e regulador (N2) | IN 281/2024 e RDC 843/2024 (DOU lido), Lei 5.768/1971, CDC (texto não reaberto), LC 214/2025 (via terceiros), CONAR 2026 (via imprensa), atos da Anvisa (via imprensa) | 12 achados |
| Dados de terceiros (N4/N5) | Momentum Works com Tabcut, EchoTik, Kalodata, Charm.io, Opinion Box, TikTok × NielsenIQ, Optimiza, Abiacom, Confi, VidMob, System1, Haus, Cruva | 13 fontes com número |
| Vídeos (YouTube) | `videos.tsv` (listados), `selecionados.tsv`, `transcricoes/` | 1.194 listados, 239 selecionados, 233 transcritos |
| Social (TikTok e Instagram) | `social/notas.md`, `social/transcricoes/` | 100 posts, 44 transcrições |
| Observação direta | `observacao/vitrine.md`: busca indireta (2026-10-15) e vitrine pública por categoria Café com sessão logada (2026-10-16, depois que o captcha foi resolvido pelo usuário) | 9 vídeos de afiliados; 50 cards e 3 páginas de produto |
| Ferramentas da pesquisa | Somadas nas 16 frentes, antes das verificações | cerca de 146 WebSearch e 330 WebFetch |

### Nível de verificação

Contagem das 192 afirmações checadas nas seções 10 (web) e 11 (navegador) das 16 notas, com o estado final depois da 2ª rodada. A classificação é aproximada, porque algumas linhas juntam mais de um id.

| Status final | Linhas | O que significa |
|---|---|---|
| CONFIRMADA | 123 | Texto oficial lido. Algumas têm ressalva (página com mais de 6 meses, ou detalhe fora do texto) |
| PARCIAL | 17 | Parte confirmada, parte sem fonte, ou duas páginas oficiais em conflito |
| CONTESTADA → valor corrigido | 24 | A fonte oficial diz outra coisa. O valor correto está neste mapa |
| SEM FONTE OFICIAL | 28 | Prática, imprensa ou case. Na maioria, não verificável por natureza |
| PENDENTE | 0 | Todas as pendências da rodada web foram lidas no navegador |

A rodada de navegador está registrada em `verificacao/resultado.tsv` (37 linhas, com trecho literal).

### Correções que a verificação impôs (vale a fonte oficial)

1. **Requisito de afiliado:** 18 anos e 1.000 seguidores, sem exigência de vídeo nos últimos 180 dias; link (Linkshare) sem mínimo. Os relatos de 5 mil e 2 mil estão superados [afil §11 A15; cases §11 R3; kid=1396756526679824, 2026-07-01].
2. **Comissão padrão por categoria existe e foi lida:** 167 subcategorias de 1% a 12%, 136 delas em 8%; Alimentos e bebidas em 8%. O "10,5% automático" não é regra [afil §11 A17; kid=3355295847515925, 2026-09-21].
3. **Taxa de comissão de Shop Ads existe no BR** (1% a 80%, opcional), com redução só depois de 30 dias e taxa sugerida pela média dos 30% melhores da categoria. O "só para convidados" está só na página global. O piso de 30% da taxa padrão não vale para Brasil e México [ads §11 R6; mix §10 A18; kid=5955311610251025, 2026-04-22].
4. **Campanha da plataforma exige GMV Max ativo.** Sem forma de pagamento, a plataforma cria anúncio com custo por pedido igual a valor do pedido ÷ ROI (ROI padrão 50 na campanha 6.6, ou seja, 2%). Não há "taxa de campanha" com esse nome [pre §11 A35; kid=3355910447433489, 2026-05-19].
5. **Proteção de ROI existe no BR**, mas os limiares (90% e 20 pedidos/dia) só estão na página global. No BR existe ainda a "Otimização de vendas líquidas" para vendedores selecionados [ads §11 R3, R8; kid=3334685477029649, 2026-09-04].
6. **Contagem de 5 minutos da LIVE Flash Sale:** a página fala em contagem de até 300 s; a obrigatoriedade não foi confirmada [live §10 R3].
7. **Suplemento em geral não aparece como "só por convite" na política de 2026-04-30**; só os de bebê, criança, gestante e pet. Uma página de 2025-12-03 diz o contrário. O que é oficial e firme: suplemento para peso ou músculo é proibido [mix §10 A4; reg §11 A22; onb §10 R8].
8. **Beleza:** exige registro Anvisa e documentos; "convite" não está escrito na seção [mix §10 A2].
9. **Always Fit é marca de suplementos**, não de moda fitness [cases §1; mix §9 item 8].
10. **GMV na Bússola de Dados (Data Compass) é o total pago pelo cliente**, não preço de tabela [ferr §11 A33; kid=6880013740476161, 2025-04-16].
11. **Reembolso sem devolução até R$ 25 "pode ser ativado"**; não é automático para todos [reg §10 A14].
12. **Teto de pedidos depois de atraso:** pela política, o marco de 50 pontos do AHR dá limite de volume (OVL) por 28 dias, não 7 [cases §10 R1].

### Como ler as citações

| Código | Arquivo |
|---|---|
| [ads] [pre] [log] [rank] [mix] [rep] [alim] [cases] | `ads/`, `preco-promocao/`, `logistica-estoque/`, `ranqueamento-vitrine/`, `produto-mix/`, `reputacao-atendimento/`, `alimentos-marca-propria/`, `cases-grandes/` (sempre `notas.md`) |
| [vid] [live] [afil] [onb] [marca] [dados] [ferr] [reg] | `conteudo-video/`, `live-commerce/`, `afiliados-criadores/`, `conta-onboarding/`, `conta-de-marca-conteudo/`, `dados-mercado-br/`, `ferramentas-analise/`, `regulatorio-fiscal/` |
| [met] [soc] [obs] [ver] | `metodo.md`, `social/notas.md`, `observacao/vitrine.md`, `verificacao/resultado.tsv` |

- "[rep A3]" é a afirmação A3 da nota de reputação; "[ads §11 R6]" é a linha R6 da verificação pelo navegador.
- "kid=" é o `knowledge_id` da Academy BR. Ids de 11 caracteres são vídeos do YouTube; ids numéricos longos são vídeos do TikTok.
- **Tipos:** [OFICIAL] regra ou número da plataforma · [PRÁTICA] o que um operador diz que faz · [CASE] números de uma operação · [DADO] estudo, ferramenta ou imprensa · [OBS] observação ou cálculo da pesquisa.
- **País:** sem marcação = Brasil. Outro país vem marcado. Regra de outro país nunca vale como brasileira.
- **"Pode estar superada":** regra com data anterior a 2026-04-15. O TikTok Shop BR abriu em 2025-05-08 e mudou tarifa, requisito de afiliado, prazos e regra de campanha várias vezes em 2026.
- **Conflito de interesse:** quase todo o conteúdo tático vem de quem vende curso, mentoria, agência ou ferramenta (13 de 15 vídeos-base em mix; 17 de 21 em cases; 19 de 22 em conta de marca). Isso está marcado nas notas.

---

## 0. A plataforma em uma página

### Como o dinheiro circula

**O que o vendedor paga em cada venda (desde 2026-07-15)** [OFICIAL]
- **Tarifa da plataforma:** abaixo de R$ 50, 10% + R$ 4 por item; de R$ 50 em diante, 6% + R$ 6 por item. A base é o preço depois do desconto do vendedor, sem o desconto bancado pela plataforma. Não há tarifa por categoria [kid=24428156307201, 2026-06-12; pre A1, A2].
- **Programa de Taxas de Envio (SFP):** 6% do preço de pedidos entregues, antes do subsídio da plataforma, com teto de R$ 50 por produto. Inscrição automática; sair tira o selo de frete grátis. A taxa não volta em devolução de pedido enviado [kid=5665577566734097, 2026-08-31; pre A5].
- **Comissão de afiliado:** é custo à parte, definido pelo vendedor por produto, com padrão de colaboração aberta por categoria (8% na maioria das 167 subcategorias). A base é o preço pago mais o reembolso do subsídio da plataforma [kid=3355295847515925; kid=1517752301717265].
- **Ads:** GMV Max, pré-pago, com meta de ROI. Toda campanha da plataforma exige GMV Max ativo [kid=3355910447433489].
- **Amostra:** produto e frete 100% do vendedor, fora do SFP [kid=6589441682917136].
- **Fora da tabela:** imposto, frete de amostra, cupom do vendedor, produção de conteúdo, agência.

**Custo da plataforma por preço do item** [OBS, cálculo sobre as duas páginas oficiais; sem Ads, cupom, imposto e frete do vendedor]

| Preço | Tarifa + SFP | % do preço | + afiliado de 8% | + afiliado de 15% |
|---|---|---|---|---|
| R$ 20 | R$ 7,20 | 36,0% | 44,0% | 51,0% |
| R$ 25 | R$ 8,00 | 32,0% | 40,0% | 47,0% |
| R$ 40 | R$ 10,40 | 26,0% | 34,0% | 41,0% |
| R$ 49,90 | R$ 11,98 | 24,0% | 32,0% | 39,0% |
| R$ 50 | R$ 12,00 | 24,0% | 32,0% | 39,0% |
| R$ 80 | R$ 15,60 | 19,5% | 27,5% | 34,5% |
| R$ 150 | R$ 24,00 | 16,0% | 24,0% | 31,0% |

- A conta é **contínua em R$ 50** (16% + R$ 4 encontra 12% + R$ 6 em R$ 12). Não existe degrau a explorar com R$ 49,90 [pre A24; alim A9].
- O peso está na **parte fixa sobre ticket baixo**. Um kit troca várias tarifas fixas por uma (2 × R$ 25 avulsos: R$ 16; kit de R$ 50: R$ 12), **se** o kit contar como 1 item. Isso não está escrito em página oficial [pre A25; ver §8].
- Em campanha, o GMV Max obrigatório a ROI 50 soma cerca de 2% do pedido [OBS sobre kid=3355910447433489].

**O que a plataforma paga**
- Cupons de frete ao comprador por nível (R$ 5 em compra a partir de R$ 109 para usuário novo, até R$ 40 a partir de R$ 159 no nível 3), descontos de campanha cofinanciados e, em campanha, aumento de comissão do criador [OFICIAL] [kid=5665577566734097; kid=2569565069149953; kid=3027449152374544].
- Reembolso sem devolução até R$ 25 coberto pela plataforma, como medida temporária [kid=894339073115921, 2026-09-24].
- Subsídio de LIVE de 20% a 30% da venda no fim de 2025 é **relato de uma marca**, sem página oficial [PRÁTICA] [cases A14; live §10 R12].

**Quando o dinheiro chega**
- Repasse Padrão em 7 dias (T+6+1), Expresso em 3 dias (SPS acima de 3,5) e Adiado em 31 dias, contados da entrega [OFICIAL] [kid=1442971112769281, 2026-06-22]. Os Termos do Vendedor falam em "até 35 a 40 dias", divergência não resolvida [reg A11].
- A comissão do afiliado sai depois da liquidação do pedido do vendedor (7, 3 ou 15 dias) [kid=1517752301717265].

### O que decide quem vende

Ordem por força da evidência. O TikTok **não publica** fórmula nem pesos de ranqueamento, nem para o feed de compras, nem para a aba Loja ou a busca [rank A2].

1. **Porta de entrada.** Categoria liberada ou por convite (alimentos, bebê, joias, auto, pet; beleza com Anvisa), CNPJ, qualificação com AHR acima de 150 e SPS acima de 4 em categoria de alto risco [OFICIAL] [kid=6504327061473040; kid=7734094290093831].
2. **Teto de pedidos da loja nova.** 50, 100 e 200 pedidos por dia até o nível Profissional, com 30 dias no mínimo e SPS de 3,0 a 3,5. Um criador grande no 1º mês faz o produto "esgotar" [OFICIAL] [kid=1444948507379472].
3. **Conteúdo que converte, em volume.** A venda nasce de uma peça (vídeo ou LIVE) ligada ao produto. Os praticantes concordam em volume de vídeos e em testar muitos ganchos; ninguém publica taxa de acerto com método [PRÁTICA] [vid §3.4].
4. **Afiliados em escala.** Nos líderes, os afiliados respondem pela maior parte do GMV: 74% da receita das melhores marcas de mercearia nos EUA [OFICIAL, fala] e entre 53% e 87% nas top 50 lojas da Europa [DADO]. Não há número do BR [marca A16, A19].
5. **GMV Max.** É o único formato de anúncio para vender no Shop desde julho de 2025, puxa sozinho os vídeos de afiliados autorizados e atribui a si todos os pedidos dos produtos promovidos, inclusive orgânicos e de afiliado [OFICIAL, global] [ads A1, A3].
6. **Saúde da loja.** SPS (desempenho relativo à categoria) e AHR (conformidade) liberam campanhas, liquidação rápida, selo e programa de afiliados. As medidas de marco "podem reduzir o tráfego", sem número [OFICIAL] [rep §2.1, §2.3].
7. **Superfície de fechamento.** Em agosto de 2025, cerca de 50% do GMV atribuído no BR fechou na aba Loja, 25,7% em vídeo e 23,4% em LIVE. Aba Loja não é busca digitada: ela recebe também quem viu o vídeo e foi comprar depois [DADO] [rank A13; dados A9].
8. **Selos.** O selo de frete grátis do SFP é o único vínculo oficial BR entre selo e exposição ("tráfego gratuito de anúncios" para qualificados, em determinados períodos) [OFICIAL] [rank A5].

### Para onde a plataforma vai

- **LIVE é a superfície que o TikTok BR mais divulga.** LIVEs por dia cresceram 20× e o GMV de LIVE 161× entre maio de 2025 e maio de 2026 [OFICIAL] [Newsroom, 2026-06-04]. A Momentum Works descreve o BR como "mais puxado por LIVE" que os EUA [DADO].
- **Ads como pedágio da escala:** campanha exige GMV Max; Ads Manager tradicional com objetivo de venda redireciona para o GMV Max [OFICIAL] [kid=3355910447433489; ads A2].
- **Recursos que já existem nos EUA e ainda não aparecem no BR:** fulfillment (FBT), assinatura por produto, Smart Promotion (taxa de 3,5% do GMV), selo "Official Shop" com verificado azul, régua pública de qualidade de anúncio [OFICIAL via terceiro, EUA] [log §2.1; alim A28; pre A31; onb A26; rank A9].
- **Logística própria em formação:** TikTok Logistics Brazil (capital de R$ 111 milhões) registrada, sem data de operação [DADO] [log A25].
- **Escala:** GMV estimado em R$ 5,3 bilhões no 1º semestre de 2026 e R$ 1,58 bilhão em junho, com 110,2 mil lojas e 2,3 milhões de influenciadores ativos [DADO, Momentum Works/Tabcut, 2026-08].

**Leitura.** A plataforma premia quem produz conteúdo que converte em volume, mobiliza criadores e aguenta o pico sem atrasar. Ela cobra pouco em percentual e muito em parte fixa no ticket baixo, e transforma Ads em condição para campanha.

---

## 1. Regras e números que importam

Só entram regras oficiais, com o status final. "Pode estar superada" = data anterior a 2026-04-15.

### 1.1 Brasil

| Tema | Regra / número (valor final) | Fonte | Data | Status |
|---|---|---|---|---|
| Tarifa | <R$ 50: 10% + R$ 4 por item; ≥R$ 50: 6% + R$ 6; base após desconto do vendedor, sem o da plataforma; antes era 6% + R$ 4 em todas as faixas | kid=24428156307201 | 2026-06-12 (vigência 2026-07-15) | CONFIRMADA |
| Tarifa "por item" | A página não diz se conta unidade, SKU ou kit; exemplos usam 1 unidade | kid=24428156307201; kid=22854025807617 | 2026-05/06 | SEM FONTE (aberto) |
| Loja nova | 0% de comissão por 60 dias, teto de R$ 17 mil, com missão, desde 2026-03-01, inclusive em análise. Cobertura da taxa fixa não dita | kid=24428156307201 | 2026-06-12 | CONFIRMADA (taxa fixa aberta) |
| SFP | 6% do preço de pedidos entregues, antes de subsídio, teto R$ 50/produto; não volta em devolução; selo em vídeo, aba Loja e LIVE; produto com "má experiência" sai da lista | kid=5665577566734097 | 2026-08-31 | CONFIRMADA |
| Base da comissão de afiliado | Preço pago + reembolso do subsídio da plataforma; reembolso parcial reduz; cancelado ou reembolsado não paga; liquidação 7/3/15 dias | kid=1517752301717265 | 2026-07-01 | CONFIRMADA (kid=2850789359355649 descreve a base de outro jeito) |
| Mudança de comissão | Aumento na hora; redução só 30 dias depois para produto vinculado; pagamento às quartas | kid=2850789359355649 | 2026-02-10 | CONFIRMADA, pode estar superada; conflita com "dia seguinte" na edição de convite (kid=6580476438529809) |
| Comissão padrão por categoria | 167 subcategorias, 1% a 12%, 136 em 8%; Alimentos e bebidas 8% (sem mudança); Cuidados com a pele 12% → 10% | kid=3355295847515925 | 2026-09-21 (vigência 2026-09-23) | CONFIRMADA |
| Comissão de Shop Ads | 1% a 80%, opcional, na colaboração aberta; desligada vale a padrão; redução após 30 dias; sugerida = média do top 30% da categoria em 30 dias; hierarquia TAP > alvo > aberta; piso de 30% não vale BR/MX | kid=5955311610251025; ads help | 2026-04-22; 2026-03 | CONFIRMADA |
| Colaboração direcionada | Até 50 criadores e 100 produtos por convite, 1.000 convites em 24 h; prevalece sobre a aberta | kid=6580476438529809 | 2025-04-14 | CONFIRMADA, pode estar superada |
| Amostra grátis | Custo do vendedor; aberta só com aprovação manual (7 dias); criador tem 14 dias; vídeo público ≥3 dias ou LIVE ≥10 min; "Criadores confiáveis" = top 20% em amostra → conteúdo | kid=6589441682917136; kid=6821109446018832 | 2026-02-05; 2025-12-30 | CONFIRMADA, pode estar superada |
| Amostra reembolsável | Meta de vendas escolhida pelo vendedor, até 3 pedidos; criador tem 60 dias; compra própria não conta | kid=3951967941150480 | 2025-07-22 | CONFIRMADA, pode estar superada |
| Criador | 18 anos, 1.000 seguidores, conta regular; sem exigência de vídeo em 180 dias; Linkshare sem mínimo | kid=1396756526679824; kid=924877269190418 | 2026-07-01; 2026-07-24 | CONFIRMADA |
| Criador: CPF e CNPJ | CPF verificado (sem isso, vitrine e vídeo ficam invisíveis); CNPJ só com nível EC ≥ L3, sem volta | kid=1415000913184513; kid=616661158987537 | 2026-09-09; 2026-07-16 | CONFIRMADA |
| CHR do criador | 0 a 1.000, começa em 200; 150 = 3 dias sem produto e campanhas; 100 = 7; 50 = 14; 0 = perde o comércio | kid=974093010454289 | 2026-01-23 | CONFIRMADA, pode estar superada |
| Agências (CAP/MCN) | Acordo de divisão de comissão com o criador (pode ser 0%); CAP envia até 100 convites/dia | kid=6810747971798800; kid=6817362679023376 | 2025-04 | CONFIRMADA, pode estar superada |
| Cadastro | Só CNPJ (MEI aceito); até 5 contas de vendedor por pessoa jurídica | kid=1721569656112912 | 2025-12-18 | CONFIRMADA, pode estar superada (FAQ de 2024-12 trazia fluxo com CPF) |
| Contas vinculadas | Individual: 1 oficial; empresarial: 1 oficial + 4 de marketing | kid=1444948507379472 | 2026-04-02 | CONFIRMADA |
| Loja nova (teto) | Iniciante 50 pedidos/dia e 1.000 anúncios; Padrão 100 (≥30 dias, ≥10 anúncios, questionário, <4 violações, SPS ≥3,0); Premium 200 (≥50 entregues, ≥10 compradores, SPS ≥3,5); Profissional ilimitado (≥100, ≥20, SPS ≥3,5); pode pular nível | kid=1444948507379472 | 2026-04-02 | CONFIRMADA (tabela lida no navegador) |
| Categorias por convite | Alimentos (petiscos, laticínios, instantâneos, frescos e congelados, bebidas não alcoólicas, confeitaria), bebê/gestante, joias, auto e moto, pet; beleza exige registro Anvisa; 14 categorias com pré-aprovação (INMETRO, ANATEL) | kid=6504327061473040 | 2026-04-30 | CONFIRMADA ("beleza por convite" CONTESTADA; suplemento geral DIVERGENTE) |
| Qualificação de alto risco | Alimentos, pet, nutrição, bebê, carro, joias: AHR >150 e SPS >4, também nas lojas associadas; Centro de qualificação, 6 etapas, só desktop | kid=7734094290093831; kid=6911810440005392 | 2026-09-29 | CONFIRMADA |
| Proibidos | Perecível, temperatura controlada, caseiro, aditivo, álcool, alimento infantil <3 anos, medicamento (inclusive isento de prescrição), herbal, "alegações de saúde", suplemento para peso ou músculo, CBD, item sem registro; exceção: embalado e bebida não alcoólica de quem cumpre a regulação | kid=6483182812481296 | 2026-08-17 | CONFIRMADA |
| Política de Conteúdo | §3.10 preço inconsistente, "menor preço", absoluto sem prova; §3.11 manipulação (inclusive de avaliações); §3.12 CTA para fora; §3.13.1 não original, marca d'água, vídeo ou LIVE sem fala, presença ou demonstração, LIVE estática ou com pré-gravado; §3.2 lance só nativo; §3.4 jogos de azar; §4.2 alimentos | kid=1413208980588305 | 2026-07-01 | CONFIRMADA |
| Conteúdo de marca | Comissão de afiliado e código promocional = conteúdo de marca, divulgação obrigatória; vitaminas não permitidas no BR | tiktok.com/legal/page/global/bc-policy/pt-BR | 2026-08-04 (vigor 2026-08-31) | CONFIRMADA (global) |
| LIVE Flash Sale | Só a conta oficial cria (contas de marketing exibem); preço ≤ menor de 14 dias (30 até 2026-01-28); 1 a 180 min (60 até 2026-02-06); de criador: 10 min a 3 dias; até 99 por comprador; elegibilidade por nota e pontos, sem número | kid=5696139560355601 | 2026-07-18 | CONFIRMADA; contagem de 5 min CONTESTADA (página: até 300 s); a página alterna "≤" e "<" |
| Prioridade de preço | LIVE Flash Sale de criador = LIVE Flash Sale > preço de campanha > Flash Sale do vendedor > desconto de produto | kid=5696139560355601 | 2026-07-18 | CONFIRMADA |
| Preço-limite de campanha | Menor histórico (L30/60/90/180D) × (1 − x%), ou % do varejo, ou comparação com outras plataformas; ficam fora do histórico cupons e subsídios da plataforma, oferta relâmpago do vendedor e promoções de vários itens | kid=3351782382814993 | 2026-02-11 | CONFIRMADA, pode estar superada ("todo cupom do vendedor fora" CONTESTADO em parte) |
| Cofinanciamento | Cupom cofinanciado mostra a divisão (ex.: 50/50); depois da inscrição, o preço só cai e o estoque só sobe | kid=2569565069149953 | 2026-02-10 | CONFIRMADA, pode estar superada |
| Campanhas | SPS ≥3,0 (desde abril de 2026) e AHR >150; sem SPS: SFCR e LDR ≤15% (ou <10 pedidos afetados); 2 SFCR seguidos = cancelamento obrigatório na seguinte; rótulo e benefícios com SPS ≥3,5 | kid=4563955062998790; kid=2996214162966289; kid=3027449152374544 | 2026-10-15; 2026-07-24; 2026-02-10 | CONFIRMADA |
| Campanha × GMV Max | Campanha da plataforma exige GMV Max pago pelo vendedor; sem ele, perde subsídio e tráfego; a plataforma cria o anúncio 7 dias antes; sem forma de pagamento, custo = pedido × 1/ROI (ROI 50 na 6.6); até 400 produtos | kid=3355910447433489 | 2026-05-19 | PARCIAL (lido no navegador) |
| GMV Max BR | Proteção de ROI existe no GMV Max original; "Otimização de vendas líquidas" (selecionados, desde 15/05, desktop): taxa por item = (pagamento + desconto da plataforma) ÷ ROI, só em pedido concluído, ROI padrão 50, sem orçamento diário e sem proteção | kid=3334685477029649 | 2026-09-04 | PARCIAL |
| SPS | 0 a 5; 3 módulos, 5 métricas (avaliação negativa 60 d; devolução por qualidade 60 d; SFCR 30 d; LDR 30 d; resposta em 24 h 60 d); nota só com 30 pedidos concluídos em 60 dias; diária; relativa à categoria; pesos só no painel; lançado em 2025-12-29 | kid=7517966208927489; kid=1074592103220993 | 2026-07-07; 2026-03-26 | CONFIRMADA |
| Faixas do SPS | >3,5: liquidação Expressa; >4,5: selo de loja de qualidade; "abaixo do padrão" (sem número): desqualifica o Marketing de Afiliados | kid=1442971112769281; kid=7517966208927489; kid=5113265534732033 | 2026-06/07 | CONFIRMADA |
| AHR (pontos do vendedor) | 0 a 1.000, começa em 200, janela de 180 dias; 150/100/50 = 7/14/28 dias sem megacampanha, novas listagens e saque; OVL de 28 dias aos 50; desativação em 0; recurso em 30 e 15 dias; correção em 12 a 72 h para algumas violações; retenção de 90 dias, permanente com fraude | kid=1444948508641040 | 2026-10-14 | CONFIRMADA |
| AHR: recuperação | Por 300 pedidos concluídos em 180 dias, com teto de 200 pontos por esse caminho; quantos pontos cada bloco vale é lido como "+1" por uma frente e não dito segundo outra | idem | 2026-10-14 | PARCIAL |
| SLA logístico | RTS recomendado em 1 dia útil; TTS em 2 dias úteis; corte 23:59:59 (UTC-3); cancelamento automático em 6 dias úteis sem "Enviado" | kid=1444948508280592 | 2026-09-30 | CONFIRMADA |
| Metas logísticas | LDR ≤4% (inclui atrasados não enviados desde 2026-03-16); SFCR ≤2,5% em 7 dias; FDR ≥90%; VTR ≥95%; amostras fora | kid=3321767214286609; kid=3333356285478657; kid=4263127323510529 | 2026-03/08 | CONFIRMADA |
| Penalidade logística | OVL (produto aparece "Esgotado"), restrição de campanha, dedução de saldo; SFCR >5% = R$ 5 por pedido cancelado, repassado ao comprador | kid=3309653722089232; kid=6133450026665749 | 2025-10-27; 2026-07-14 | CONFIRMADA (OVL pode estar superada) |
| Recurso logístico | Lista fechada (coleta, ponto fechado, feriado municipal, sistema, força maior, pedido do cliente); viral, campanha e falta de estoque não entram | kid=3026645972993808 | 2026-03-06 | CONFIRMADA, pode estar superada |
| Modelos de envio | Envio pelo TikTok é o padrão; envio pelo vendedor com aprovação; dropshipping e logística internacional proibidos; pick-up em 48 h; correção de rastreio em 72 h | kid=1442971111884545 | 2026-03-06 | CONFIRMADA, pode estar superada |
| Devolução | 30 dias por qualquer motivo nas categorias elegíveis, 90 em defeito; frete de volta pago pelo TikTok em "não preciso mais" e tamanho, pelo vendedor em defeito, erro, falta e atraso; alimentos, bebidas, cosméticos e perfumes só lacrados; reembolso sem devolução até R$ 25 "pode ser ativado" | kid=894339073115921 | 2026-09-24 | CONFIRMADA ("automático" CONTESTADO); diverge de kid=2578485181925121 |
| Alimento não retornável | Ingerível não volta; decisão de reembolso em 72 h | kid=2578485181925121 | 2026-04-14 | CONFIRMADA, mas a página mais recente (2026-09-24) manda devolver lacrado |
| Repasse | Padrão 7 dias, Expresso 3 (SPS >3,5), Adiado 31 | kid=1442971112769281 | 2026-06-22 | CONFIRMADA; Termos dizem até 35 a 40 dias |
| Chat | Resposta em 24 h ≥70%, resolução ≥65%, satisfação ≥75%, janela de 7 dias | kid=2583022047233809 | 2025-09-30 | CONFIRMADA, pode estar superada |
| Avaliações | Proibido oferecer cupom, dinheiro ou produto por avaliação positiva ou alterada; reembolso pelo chat sai como "vendedor não tem culpa" e não afeta o SPS | kid=7279248559163144; kid=696094993368849 | 2026-07/08 | CONFIRMADA |
| Nota fiscal | NF-e antes do envio; emissor nativo só MEI e Simples; o TikTok emite só a nota das próprias tarifas e um demonstrativo das comissões | kid=4896169624913680; kid=1487157475673872; kid=24428156389121 | 2025-09; 2025-05; 2026-02 | CONFIRMADA, pode estar superada |
| GMV no painel | GMV da Bússola de Dados = total pago pelo cliente; valor recebido em Finanças (Liquidação) | kid=6880013740476161 | 2025-04-16 | CONFIRMADA, pode estar superada |
| Vitrine do criador | Até 2.000 produtos; organização inteligente; selo de risco por avaliação negativa e preço acima dos concorrentes | kid=6825383530710785 | 2025-04-14 | CONFIRMADA, pode estar superada |
| Anúncio | Quantidade, cor e design iguais entre título, imagem e SKU; variante aleatória no título e no SKU | vídeo oficial 7678673969184230677 | 2026-08-27 | CONFIRMADA |
| Contas | Proibido comprar, vender ou transferir loja; reverificação de identidade em caso de risco | kid=3039191651075856; kid=1984591137818385 | 2026-02/03 | CONFIRMADA, pode estar superada |

### 1.2 Global (sem país na página) e EUA

| Tema | Regra / número | Fonte | Data | País | Status |
|---|---|---|---|---|---|
| Formato único | GMV Max é o único tipo de Shop Ads desde julho de 2025; campanhas antigas seguem ativas | ads help gmv-max-migration | 2026-03 | global | CONFIRMADA |
| Atribuição | Todos os pedidos dos produtos promovidos vão para o GMV Max, orgânicos ou pagos, com ou sem interação; janela de 1 dia no exemplo; produto não promovido fica fora | about-product-gmv-max; about-attribution-for-gmv-max | 2026-09; 2026-06 | global | CONFIRMADA (a página de atribuição não cita afiliado; a do produto cita) |
| Proteção de ROI | Crédito quando o ROI do dia fica abaixo de 90% da meta e há mais de 20 pedidos/dia; perde com edição manual da meta, produto editado, pausa, entrega máxima e verba de boost | about-roi-protection | 2026-09 | global (existência no BR confirmada) | CONFIRMADA |
| Entrega máxima | 3 a 5 dias na partida a frio, orçamento ≥10× o ticket médio, +30% por dia | best-practices-for-max-delivery | s/d | global | CONFIRMADA |
| Meta de ROI | ROI = GMV não-LIVE histórico ÷ custo; orçamento = 2× GMV ÷ meta; consumo <80%; manter a meta 3 dias; incluir todos os produtos | best-practices-for-product-gmv-max | 2026-06 | global | CONFIRMADA |
| Conta de anúncios | Uma conta principal por loja; trocar pausa as campanhas | gmv-max-guidelines | 2026-06 | global | CONFIRMADA |
| Vídeo de afiliado | Recebe rótulo comercial em campanha; se o criador desliga a autorização, os anúncios pausam | about-product-gmv-max; faqs-affiliate-creatives | 2026-09; 2026-03 | global | CONFIRMADA |
| Relatório de criativo | Visualização de 2 s e 6 s, quartis, clique, CVR; julgar pela receita bruta, porque ROI e custo por pedido incluem orgânicos | how-to-see-reporting | 2026-06 | global | CONFIRMADA |
| Data Compass | Atribuição padrão de 7 dias após clique ou 1 dia após visualização; receita bruta = pago − imposto + desconto da plataforma; seis cortes Ads × afiliado | about-ads-metrics-in-seller-center | 2025-02 | global | CONFIRMADA, pode estar superada |
| ROI "Pro" | Desconta afiliado, cupom e tarifa; "em teste" no blog pt-BR; lançado como GMV Max Pro na América do Norte; PDF oficial lista 16 países com Brasil, sem dizer que recurso vale onde | blog pt-BR; Ua8Zgb2WxxI; TikTok_GMV_Max.pdf | 2026-05-13; 2026-07-28 | pt-BR / EUA-Canadá | PARCIAL |
| Volume de criativo | "50 a 70 vídeos, 5 a 10 por dia" não tem fonte; o guia F&B pede 5 a 10 vídeos no início e 2 por semana; o blog pt-BR diz "sem exigência mínima" | FnB_cold_start_EN.pdf; blog pt-BR | s/d; 2026-05-13 | EUA/SEA; pt-BR | CONTESTADA |
| LIVE GMV Max | Otimiza a maior receita bruta da LIVE ou o ROI da sala; pausa os LIVE Shopping Ads da conta oficial | about-live-gmv-max | 2026-09 | global | CONFIRMADA (com ajuste) |
| SPS EUA | 6 métricas, 30 pedidos em 90 dias, decaimento de 0,7 a cada 15 dias, abaixo de 3,0 perde afiliados | ppc.land | 2026-06-22 | EUA | via terceiro |
| AHR EUA | Substituiu os Violation Points em julho de 2026; 4 pontos por 200 pedidos | ppc.land | 2026-06-29 | EUA | via terceiro |
| Smart Promotion | 3,5% do GMV da loja (4,5% em megacampanha), obrigatório para campanhas e Flash Sale desde abril de 2026 | ppc.land | 2026-06-22 | EUA | via terceiro |
| Alimentos EUA | Validade mínima na entrega: snacks 90 d, instantâneos 180 d, bebidas, chá e pó 270 d; assinatura por produto com 5% a 20% de desconto | ppc.land; startupfortune | 2026-06; 2026-07 | EUA | via terceiro |
| Qualidade de anúncio | Poor/Fair/Good; título de 25 a 255 caracteres; 5 ou mais imagens acima de 600×600; teto Fair sem atributos da categoria; a página não liga a faixa à exposição | seller-us kid=481891871868714 | 2026-08-07 | EUA | CONFIRMADA (versão BR dá 404) |
| Pontuação do criador | 2,5 alcance ampliado; 3,5 recursos de visibilidade; 4,0 e 4,5 selos; sem percentual | ppc.land | 2026-06-08 | EUA | via terceiro |

---

## 2. Por frente: o que os melhores fazem

Em cada frente, "regra" é N1 e "prática" é praticante, quase sempre com confiança C. Nenhuma prática tem teste controlado público no BR.

### 2.1 Ads (GMV Max)

- **Mecânica:** o vendedor controla produto, orçamento e meta de ROI (ou entrega máxima); público, lance e criativo ficam com o algoritmo [PRÁTICA, consenso] [ads §1 item 2]. Com meta de ROI, o orçamento é teto; com meta alta demais, a campanha não gasta [PRÁTICA] [ads §6 item 2].
- **ROI de equilíbrio:** preço ÷ margem antes de Ads; meta "equilibrada" de 1,5× a 2× o equilíbrio [PRÁTICA] p7BZwvm2Y_c (EUA). Com a tarifa BR, um item de R$ 40 (CPV hipotético R$ 15, comissão de anúncio de 5%) empata a ROI 3,17; um de R$ 80 (CPV R$ 30) a 2,63; com 10% de imposto, 4,65 e 3,57 [OBS] [ads §2.6]. Parte dos pedidos atribuídos paga a comissão orgânica, não a de anúncio, o que puxa o equilíbrio real para cima.
- **Antes de ligar:** estoque de vídeos (de 25 por semana a 50 por produto, conforme a fonte), produto com sinal orgânico, catálogo sem ruptura, preço já com comissão e amostra, afiliados como "motor de criativos" [PRÁTICA] [ads §3.1].
- **Lançamento, divergência:** meta baixa (0,1 a 1) ou entrega máxima para comprar dado [PRÁTICA] (Kilgour, 5x Dashboard, EUA) e oficial (entrega máxima), contra meta de 1,5× a 2× o equilíbrio desde o 1º dia [PRÁTICA] (Reiter, EUA) [ads §3.2].
- **Manutenção:** "orçamento com frequência, meta raramente, produto quase nunca"; manter a meta 3 dias [PRÁTICA; OFICIAL] [ads §3.2]. Edição manual tira a proteção de ROI do dia [OFICIAL].
- **Estrutura, divergência:** praticantes usam poucos produtos do mesmo comprador por campanha; a orientação oficial manda incluir todos [ads §3.3]. Que um produto só caiba numa campanha não tem fonte oficial [ads §10 R10].
- **Criativo:** seleção automática é a regra oficial; os praticantes excluem vídeos com gasto relevante abaixo da meta e dão boost aos de ROI alto e gasto baixo, contra a orientação oficial de não retirar vídeo só porque gasta muito [ads §3.4].
- **Comissão de anúncio:** taxa separada (1% a 80%). No BR, praticantes usam de 1% a 5% contra 8% a 10% orgânicos; nos EUA, cerca de metade da orgânica. Comissão de anúncio baixa afasta criadores [PRÁTICA] [ads §3.6].
- **Leitura do painel:** o ROI do GMV Max inclui orgânico e afiliado; não é ROAS de mídia [OFICIAL]. Devolução e comissão podem zerar um "ROI 4" [PRÁTICA] YOSCEWDEstE (EUA).
- **Dois casos de ROI ≈ 15** (BR e EUA) são um produto no pico, com orgânico dentro do número [CASE] [ads §4.5].

### 2.2 Preço e promoção

- **Consenso:** precificar pela margem depois do afiliado, não pela tarifa. Precificar sem afiliado e vender com afiliado gerou margem negativa em painel real [CASE] px_vzMN9W5Y [pre §3.1]. Meta citada de margem de contribuição: 10% a 20% [PRÁTICA].
- **Kit e bundle** para diluir a tarifa fixa e subir o ticket: "o nosso forte é kit" numa operação de 1.000 pedidos/dia; kit de 3 a R$ 50 em LIVE na Black Friday 2025 [CASE] KMZ8gimnMhc; z-Nq9_kLbQ8.
- **Preço por canal dentro do TikTok:** LIVE Flash Sale vale só no canal da LIVE; Flash Sale de criador dá preço próprio a cada criador; isso cria preço exclusivo sem mexer no preço público [OFICIAL] [pre §3.3].
- **Proteger o piso:** baixar o preço de lista reduz o menor histórico, que vira piso da próxima campanha (L30 a L180) e da LIVE Flash Sale (14 dias). Ferramentas fora do histórico (oferta relâmpago do vendedor, promoções de vários itens, cupons e subsídios da plataforma) preservam o piso [OFICIAL + OBS] [pre §2.5].
- **Campanhas pagas pela plataforma:** missões liberam cupons pagos pela plataforma (painel: 40 cupons de R$ 12 em pedido ≥R$ 80) [PRÁTICA, painel] NmB4AUNfVwk. Cupom cofinanciado divide o custo; "100% bancado" não foi confirmado em página oficial [mix §10 A22].
- **Calendário:** datas duplas todo mês; Liquida 10.10 com R$ 20 milhões em cupons [OFICIAL] 7691075511245737217; Black Friday 2026 de 27/10 a 12/12 com R$ 100 milhões em cupons, divisão de custo não divulgada [DADO, só imprensa] [pre A19].
- **Efeito de promoção:** o +129% de GMV da Black Friday 2025 é contra o 10/10, outra data promocional, sem controle [OFICIAL] [Newsroom 2025-12-02].
- **Reação à tarifa de julho, divergência:** "não fazer nada" contra cortar comissão de afiliado (20% → 15%) [PRÁTICA]; nenhum dado.

### 2.3 Logística e estoque

- **Consenso:** despachar antes do prazo (fábrica de camisetas leva pacotes ao ponto 3 vezes ao dia) [CASE] KMZ8gimnMhc; estoque real e ERP integrado (Bling, Tiny, UpSeller) com NF-e automática [PRÁTICA]; provar tudo com data e hora, que é o que a lista oficial de recurso pede [OFICIAL].
- **Pico viral:** Always Fit passou de cerca de 1.000 para mais de 10.000 pedidos/dia no 10/10/2025, atrasou e caiu num teto de 1.000 pedidos/dia; perda estimada de R$ 1 a 1,5 milhão; afiliados migraram para concorrentes [CASE, fala dos sócios] z-Nq9_kLbQ8; 6sWUmzRywWU. Pela política, o OVL faz o produto aparecer "Esgotado" e zera a cada dia [OFICIAL].
- **Resposta dos grandes:** catálogo curto no TikTok (8 a 10 SKUs contra mais de 80 no site), várias fábricas (a Always Fit cita 48 terceiras), rótulo em prazo curto, operador logístico com WMS, troca de operador em 3 dias [CASE] [log §3.2].
- **Penalidade atinge o afiliado:** com o carrinho travado, a comissão dos afiliados para [PRÁTICA; CASE].
- **Não há fulfillment no BR**; vídeos dublados dos EUA que vendem FBT trocam o país [DADO; OBS] [log §6].
- **Lacuna central:** nenhum dado agregado de ruptura, LDR médio ou prazo de entrega do TikTok Shop BR [log §9].

### 2.4 Ranqueamento, busca e vitrine

- **Oficial é pouco:** fatores gerais do Para Você (2020, global: interações pesam mais que legenda e hashtag), selos da vitrine BR, selo de frete grátis com tráfego para qualificados, superfícies do GMV Max. Não há parâmetros oficiais da aba Loja nem da busca [rank A1 a A8].
- **SEO de produto (consenso de praticantes, quase todos dos EUA, sem teste):** palavra principal no começo do título, sem adjetivo promocional; categoria mais específica; atributos completos; cauda longa do autocompletar da busca do app; palavra dita e escrita no vídeo [PRÁTICA] [rank A27, A28].
- **Diagnóstico pelo funil:** impressões caindo junto com clique e conversão = entrega; muitas impressões e pouco clique = título e capa; muitas visitas e pouco pedido = imagens, avaliações e preço contra concorrente [PRÁTICA] [rank §3.5].
- **Busca ou descoberta, divergência:** "não é plataforma de busca" (praticantes BR) contra "virou buscador" (agências EUA). Os 50% da aba Loja dão razão parcial aos dois; ninguém publicou a divisão entre busca digitada e navegação [rank §3.6].
- **Mitos derrubados:** "+10% de visibilidade a 2,5" (sem fonte; os limiares são da pontuação do criador nos EUA); "Poor e Fair são suprimidos" (a página oficial não diz); "48% a 65% das vendas vêm da busca" (blog sem fonte) [rank §6].

### 2.5 Produto e mix

- **Filtro de seleção (consenso):** demonstrável em câmera, resolve um problema visível, ticket de impulso, comissão atraente; produto que renda muitos ângulos ("capacidade de repetição") [PRÁTICA] [mix §3.2; met §7.4].
- **Pesquisa nas ferramentas:** GMV de 30 dias, crescimento estável de 20% a 100% (rejeitar 999%), número de criadores e concentração do GMV nos 3 maiores (Kalodata); pico contra demanda pela dispersão em 5 ou mais criadores e pela curva de 30 dias contra a de 7 dias [PRÁTICA] [mix §3.3].
- **Sortimento dos grandes:** um anúncio-herói com variações de entrada e premium, para somar vendidos e avaliações (Medicube, Bloom, EUA); menos de 1% dos produtos faz cerca de 50% da receita (fala do TikTok EUA) [PRÁTICA; OFICIAL-EUA] [mix §3.5].
- **Tese da líder BR:** "lançar 100 produtos" e deixar o que valida virar perpétuo; nº 1 é um kit [CASE] 6sWUmzRywWU; z-Nq9_kLbQ8.
- **Divergência principal:** comissão aceitável pelo afiliado (8% a 10% no BR; 15% a 20% mínimo nos EUA). A tabela oficial BR põe a maioria das categorias em 8% [mix A17; afil §11 A17].
- **Racionalização:** poucos SKUs; lucro líquido por SKU depois de amostra, tarifa, comissão e Ads como métrica-líder [PRÁTICA, EUA] oPqx01hQcTY. Nenhum case BR mostra corte de SKU com dado.

### 2.6 Reputação e atendimento

- **Dois placares:** SPS (desempenho relativo à categoria) e AHR (conformidade). O mesmo atraso pesa duas vezes: derruba o SPS e gera violação no AHR [OFICIAL] [rep §2.3].
- **Consenso:** um dono da saúde da conta que revisa os módulos uma ou duas vezes por semana e recorre de toda violação [PRÁTICA, EUA] s2xtJVLtHHg; conferir notificações todo dia (a política pede) [OFICIAL]; embalagem por tipo de produto e conferência em duas etapas [OFICIAL]; mexer primeiro na métrica mais longe do benchmark da categoria (recomendação oficial do diagnóstico) [rep §3.1].
- **Avaliação:** cupom condicionado à avaliação "dobrou" as avaliações num relato [PRÁTICA] wS2Lbc7XSBo; a política proíbe incentivo por avaliação positiva ou alterada [OFICIAL]. Lembrete sem incentivo não aparece como proibido [rep §3.3].
- **Reembolso negociado pelo chat** não pesa no SPS desde agosto de 2026 [OFICIAL] kid=696094993368849.
- **Divergências:** se violação reduz alcance (relatos se contradizem; a página diz que medidas de marco "podem reduzir o tráfego"); meta de chat "oficial de 98%" (não confirmada; a página BR diz 70%) [rep §3.3].

### 2.7 Alimentos e marca própria

Detalhe na §6. Em resumo: categoria por convite, qualificação com AHR >150 e SPS >4, alegações de saúde travadas, afiliado como motor nos EUA, recompra construída fora da plataforma pelas marcas de consumível, e nenhum número público de GMV de alimentos no BR [alim §1].

### 2.8 Cases grandes

- **Não há ranking verificável de lojas do BR.** Os cases vêm de release da plataforma (Natura, Johnson's Baby, Riachuelo, BigHome, Moderna), de fala de fundador (Always Fit) ou de ferramenta N5 [cases §1].
- **Alavancas que se repetem entre fontes independentes:** exército de afiliados (de 9 mil a 90 mil) com comunidade e gestor dedicado; amostra em escala (de 5 mil a 20 mil por mês); LIVE; poucos SKUs no canal; volume de vídeos (mais de mil por dia em marca grande); estoque e fábrica alternativa antes de escalar [cases §3.1].
- **O gargalo é estoque e logística**, mais que marketing (Always Fit no BR; JoySpring e Dr. Melaxin nos EUA) [CASE].
- **O financeiro é difícil de ler:** "cinco painéis, cinco faturamentos"; perda de R$ 20 a 40 mil por dia "sem saber" [CASE] z-Nq9_kLbQ8.
- **Lucro no canal:** grandes dos EUA operam no equilíbrio ou abaixo e justificam com transbordamento para a Amazon, sem teste causal [CASE, EUA]. Duas marcas BR dizem não ter lucro no TikTok [CASE] KQZ3L7nXd0M; YixvoQkAiNQ.
- **O TikTok Shop nem sempre é o maior canal do líder:** a Always Fit diz que o canal fica abaixo da metade da receita em 2026-10 [CASE].
- **Super Brand Day existe no BR por convite** (Granado, Riachuelo), sem página de requisitos [OFICIAL; imprensa].

### 2.9 Conteúdo e vídeo

- **Regra que mais pega a prática:** a política BR chama de baixa qualidade o vídeo ou LIVE em que o criador não fala, não aparece ou não demonstra o produto (§3.13.1). Isso colide com o "POV sem fala" e o avatar de IA vendidos por mentores BR [OFICIAL; PRÁTICA] [vid A1].
- **Estrutura dominante (8 de 15 transcrições):** gancho (visual, falado e texto) → dor → produto em uso → prova → oferta e escassez → CTA ao carrinho laranja [PRÁTICA] [vid A22].
- **O gancho tem de atrair comprador:** o mesmo corpo de roteiro rendeu US$ 160 mil e US$ 3 mil conforme o gancho [CASE, EUA] J3quLmejc7g.
- **Volume:** 10 a 20 vídeos por dia por afiliado, 960 a 10 mil posts por mês por marca; taxa de acerto descrita como lei de potência (90/10, 80/20), sem método [PRÁTICA, EUA e BR] [vid §3.4].
- **Medição:** pela venda, não por views. Nos vídeos citados como prova, o GMV por mil views varia 20× [OBS] [vid §4].
- **Reaproveitamento:** GMV Max com vídeos autorizados, código Spark para os demais, direito de uso para Meta [PRÁTICA]. Repost sem edição criativa nova conta como "mídia importada" [OFICIAL].
- **Divulgação:** nenhum dos 15 tutoriais menciona a chave de conteúdo de marca, obrigatória desde 2026-08-31 [OBS] [vid §6 item 12].

### 2.10 Live commerce

- **Regras:** LIVE Flash Sale só pela conta oficial, preço ≤ menor de 14 dias, 1 a 180 min; versão de criador de 10 min a 3 dias [OFICIAL]. Proibidas LIVE estática, pré-gravada ou sem fala, interação e presença [OFICIAL] kid=1413208980588305.
- **Roteiro curto e repetido**, porque o público troca em segundos: ciclos de 50 s a 3 min no BR, 5 a 8 blocos nos EUA [PRÁTICA] [live §3.2].
- **Apresentador + operador** (fixa produto, solta Flash Sale, responde chat) [PRÁTICA] [live §3.5].
- **Mega LIVE é instrumento de marca:** Natura com LIVE de 12 h e +228% de conversão de carrinho abandonado; 52 mil LIVEs em 2025, 60% de consultoras; Johnson's Baby com 727 h de LIVE de afiliados [OFICIAL, cases da plataforma].
- **Divergências:** oferta ou apresentador; LIVE própria ou só de afiliados (um fabricante pausou 3 estúdios por ROI; uma marca deixou a LIVE para os afiliados, porque promoção maior na LIVE da marca os afasta) [CASE; PRÁTICA] [live A30, A31].
- **Leitura pelo funil:** numa LIVE BR de 3 h, 42 mil views, R$ 32.785, entrada na sala ≈ 4%, pedido 0,45%, 79% de não seguidores [CASE] AJOAtisYWtM.

### 2.11 Afiliados e criadores

- **Os líderes tratam criadores como força de vendas:** Always Fit com 90 mil afiliados e cerca de 5 mil amostras por mês (depois de 15 a 20 mil no início) [CASE] 6sWUmzRywWU; Moderna com mais de 9 mil afiliados ativos [OFICIAL].
- **Recrutar:** colaboração aberta como ímã; garimpo dos criadores do concorrente pela "análise de afiliados" da loja numa ferramenta; filtros por GMV de 30 dias, views médias e taxa estimada de postagem (70% a 80% ou mais); seguidores são "métrica enganosa" [PRÁTICA, EUA] AD32WdQGXRY.
- **O gargalo é a retenção:** 50% a 60% dos criadores com amostra postam uma vez só (ferramenta dos EUA, com conflito); 35% a 40% das amostras não viram vídeo (agência BR) [PRÁTICA] [afil A25, A26].
- **Alavancas de retenção:** comissão VIP ou em escada, fixo por LIVE (R$ 50 a 100 no BR), prêmio por produção, retainer para os melhores, concursos, comunidade em WhatsApp ou Discord, brief renovado todo mês [PRÁTICA] [afil §3.5].
- **Premiar volume ou venda, divergência:** concurso por volume gerou 200 vídeos com cerca de US$ 100 de GMV [CASE, EUA] 1S-Sf8v8ZfY.
- **Tributação:** criador PF até o nível L3; NF da comissão para cada vendedor, segundo FAQ vista só em print de vídeo (outro contador diz o contrário) [OFICIAL; PRÁTICA] [reg §2.3].

### 2.12 Abertura e onboarding

- **Sequência dos primeiros 90 dias (consenso de ordem, números divergentes):** base operacional (ERP, NF-e, armazém de coleta e devolução, conta PJ no mesmo CNPJ) → catálogo curto com vídeo na listagem → colaboração aberta e amostras filtradas → GMV Max depois de centenas de vídeos → LIVE mais tarde [PRÁTICA] [onb §3.2].
- **O teto de 50 a 200 pedidos/dia limita os playbooks "agressivos" dos EUA** (1.000 amostras por SKU no mês 1), que não mencionam esse teto [OBS] [onb §3.2].
- **Erros documentados:** criador grande no nível Iniciante; estoque fictício; violação no 1º mês (4 em 30 dias travam o nível); não chegar a 30 pedidos em 60 dias (fica sem SPS); dados divergentes no cadastro [OFICIAL; PRÁTICA] [onb §6].
- **Comissão inicial:** começar mais baixo e subir custa menos que começar alto e esperar 30 dias para baixar [OBS sobre kid=2850789359355649].

### 2.13 Conta da marca e conteúdo

- **Na maioria dos líderes, a conta própria é a menor parte do GMV:** 17,6% em alimentos nos EUA; de 7,3% a 34,3% nas top 50 lojas da Europa [DADO, Kalodata]. Não há número BR [marca A18, A19].
- **A plataforma desaconselha depender só de afiliados:** conteúdo comprável é fração pequena do feed por desenho; o guia F&B pede ao menos 2 vídeos próprios por semana e diz que lojas com 100 ou mais vídeos escalam melhor no GMV Max [OFICIAL, EUA/SEA] [marca A15, A17].
- **Funções só da conta oficial:** LIVE Flash Sale; Super Brand Day e campanha de marca são por convite [OFICIAL].
- **Pessoas da empresa como criadoras:** consultoras (Natura), gerentes de produto (Granado), artistas próprios e clientes de fidelidade como afiliados (MAC), sócio como afiliado nº 1 (Maxfen) [CASE] [marca §3.3].
- **Briefing, não roteiro** (consenso), com divergência: roteiros diários (Ridge) e narrativa copiada ao pé da letra (Maxfen) [PRÁTICA; CASE].
- **A conta como hub:** responde comentários com vídeo, entra nas LIVEs de afiliados, lidera a comunidade fora da plataforma e reaproveita conteúdo na Meta [CASE] [marca §3.1].

### 2.14 Dados de mercado

- **O TikTok só divulga multiplicadores:** GMV médio diário 102×, afiliados ativos 46×, LIVEs 20×, GMV de LIVE 161× no 1º ano [OFICIAL] [Newsroom 2026-06-04]. Em setembro contra maio de 2025: GMV diário 26× [OFICIAL] [Newsroom 2025-11-06].
- **Tamanho em faixa:** Momentum/Tabcut dá R$ 5,3 bilhões no 1º semestre de 2026; EchoTik dá cerca de metade; reconciliando o 102× com a base de lançamento, R$ 0,7 a 1,6 bilhão por mês no 2º tri de 2026 [DADO; OBS] [dados §4.1].
- **Fatia do e-commerce:** de 2,5% a 4,2% conforme o denominador (Confi R$ 208,4 bilhões ou Abiacom R$ 125 bilhões no semestre) [OBS].
- **Comprador:** 31% dos usuários já compraram no Shop e 43% pretendem; entre compradores, 49% já procuravam o produto, 44% compraram por vídeo de criador, 20% em LIVE; 11% compraram alimentos e bebidas, a menor fatia [DADO, Opinion Box, n = 1.066, ±3,1 p.p., jan/2026].
- **Mitos:** "R$ 37 bilhões no PIB" é efeito da publicidade, não do Shop; "3º maior marketplace", "12º país", "ticket médio de R$ 47" e "134 milhões de usuários" não têm fonte oficial [dados §6; dados §11 A4].

### 2.15 Ferramentas de análise

- **Nenhuma ferramenta publica fórmula.** Só a Cruva declara erro (cerca de ±30%) e admite que subconta criadores pequenos [DADO] [ferr A1].
- **O dado nativo separa o que nenhuma ferramenta separa:** a Visão geral do Data Compass divide a receita em Ads, não Ads, Ads com e sem afiliado, afiliado sem Ads e nenhum dos dois [OFICIAL, global, 2025-02] [ferr A8].
- **Fluxo das agências:** produto → criadores do produto → vídeos (selo AD) → LIVE → loja concorrente → análise de afiliados do concorrente para convidar os mesmos criadores [PRÁTICA] [ferr §3.1].
- **Selo "AD", divergência compatível:** o vídeo convenceu a loja a pagar, mas as views não servem de meta orgânica [ferr §3.7].
- **Teto de outreach:** faixas semanais por GMV de afiliados vêm de fornecedores dos EUA; o "200 novos criadores por dia" é fonte única; a única cota oficial BR achada é a da CAP (100 por dia) [ferr §11 A16, A17].
- **Sinais de fonte fraca:** link de afiliado da ferramenta (a FastMoss paga 15% a 30% recorrentes), revenda de "Kalodata ilimitado", tutorial que ensina a burlar o limite gratuito [ferr §1 itens 13, 14].

### 2.16 Regulatório e fiscal

- **Vendedor emite a NF da venda e recolhe os tributos;** o TikTok não recolhe imposto sobre as vendas [OFICIAL] kid=1487157475673872.
- **Rótulo comercial cobre comissão de afiliado** (TikTok) e, para o CONAR 2026, comissão por desempenho já é publicidade, com anunciante e agência orientando o criador [OFICIAL; N2 via imprensa] [reg A19, A21].
- **Três camadas de responsabilidade por alegação:** plataforma (remoção, pontos, retenção), CONAR, CDC (ônus da prova do anunciante; STF: marketplace responde pelo CDC, com responsabilidade presumida em anúncio pago) [reg §2.5].
- **Sorteio em LIVE:** proibido pela política (jogos de azar, §3.4) e, fora dela, sujeito à Lei 5.768/1971 [OFICIAL; N2].
- **Reforma tributária:** a plataforma responde solidariamente pelo IBS e pela CBS se o vendedor não emitir documento fiscal (LC 214/2025) [N2 via terceiro].
- **Não há vendedor cross-border no TikTok Shop BR;** pagamentos só domésticos [OFICIAL].
- **Divergências abertas:** afiliado pode ser MEI (CNAE 7490-1/04); nota da comissão para o vendedor ou para o TikTok; repasse 7/3/31 contra 35 a 40 dias [reg §3].

---

## 3. Benchmarks

**Aviso.** Não existe benchmark brasileiro com amostra de CPM, CTR, CTOR, GPM, conversão de LIVE, ROI de GMV Max, taxa de devolução ou distribuição de SPS. O que segue é o que existe, separado por qualidade.

### 3.1 Com amostra ou método declarado

| Número | Método e amostra | Fonte | Data | País | Leitura |
|---|---|---|---|---|---|
| GMV do 1º sem/2026 ≈ R$ 5,3 bi; junho R$ 1,58 bi; 110,2 mil lojas; 2,3 mi influenciadores; 3,5 mil lojas acima de US$ 1 mi | Dados de plataforma da Tabcut + pesquisa Momentum; erro não declarado | momentum.asia | 2026-08 | BR | Melhor estimativa pública; ler como faixa |
| GMV mensal de 2025: US$ 1; 10,1; 25,7; 46,1 mi (mai a ago) | Tabcut | InfoMoney; thelowdown | 2025-09 | BR | Curva de lançamento |
| Ago/2025: aba Loja ≈ 50%, vídeo 25,7%, LIVE 23,4%; beleza 21,26% | Tabcut via Momentum | thelowdown | 2025-09-08 | BR | Pode estar superado |
| EUA 1º sem/2026: aba Loja 51,4%, vídeo 40,4%, LIVE 8,2% | Tabcut via Momentum | thelowdown | 2026-08-06 | EUA | Comparação de mix |
| 31% já compraram; 11% dos compradores compraram alimentos e bebidas; 49% já procuravam o produto | Opinion Box, n = 1.066, ±3,1 p.p. | via viniensina e Stone | jan/2026 | BR | Mede usuário declarando, não GMV |
| Pessoa falando para a câmera: +14% na visualização de 2 s | VidMob × TikTok, 1.678 anúncios | via clouted.com | 2026-07 (dados de 2023) | global | Anúncio, não Shop |
| Anúncio de criador: +23% de memória de marca | System1 × WPP × TikTok, 1.217 anúncios, 182.550 usuários | via clouted.com | s/d | global | Anúncio, não Shop |
| Erro de estimativa ≈ ±30% | Cruva, declaração do método | cruva.com | s/d | — | Única ferramenta que declara erro |
| E-commerce do 1º sem/2026: R$ 125 bi (Abiacom) × R$ 208,4 bi (Confi) | Associação × consultoria | imprensa | 2026-07/08 | BR | Denominadores divergem 67% |
| Alimentos EUA: US$ 215 mi jan–jul/2026 (≈2%); afiliado 73,9%, conta própria 17,6%; vídeo 65,8%, LIVE 21,2% | Kalodata (N5) | via wearemada | 2026-09 | EUA | Diverge da Charm.io (6,9% em 2025); não somar |
| Conta própria nas top 50 lojas: 7,3% (Espanha) a 34,3% (Itália) | Kalodata, snapshot de um mês | via Netpeak | 2026-04 | Europa | Só direção |

### 3.2 Da própria plataforma, sem método publicado

| Número | Fonte | Data | País |
|---|---|---|---|
| 102× GMV diário; 46× afiliados ativos; 20× LIVEs; 161× GMV de LIVE | Newsroom | 2026-06-04 | BR |
| 57,8% concluem compra no Shop depois de descobrir no app (in-app, 17 mil) | Newsroom | 2026-06-04 | BR |
| Black Friday 2025: GMV +129% e LIVE +143% contra o 10/10 | Newsroom | 2025-12-02 | BR |
| 91% acham a LIVE a melhor forma de tirar dúvidas; 82% acham a entrega rápida (n = 1.002) | TikTok × NielsenIQ via Mercado & Consumo | 2026-10-01 | BR |
| GMV Max: +15% de receita (impacto causal modelado, 11 clientes); +20% (testes internos); +30% (EUA 2024) | blogs e Newsroom TikTok | 2025-11; 2026-05; 2025-01 | Reino Unido; s/d; EUA |
| Quem usa Shop Ads tem GMV mediano 112% maior (correlação) | webinar tGotPuBPS08 | 2026-02-24 | EUA |
| ≈ 50% do GMV de alimentos vem de vídeos com mais de 30 dias, quase sempre com Ads | idem | 2026-02-24 | EUA |
| LDR ≤ 3% para nota ≥ 4 e 8% para nota ≤ 1 (exemplo de uma categoria) | webinar LATAM kid=1074592103220993 | 2026-03-26 | BR |

### 3.3 De praticante (um caso cada; não é meta)

| Número | Fonte | Data | País |
|---|---|---|---|
| ROI ≈ 15; R$ 12 mil de gasto em 3 meses; ≈ R$ 194 mil de GMV; 367 criativos; ticket ≈ R$ 50 | EgC3pol8iV4 (agência) | 2026-07-02 | BR |
| Comissão orgânica praticada 8% a 15%; de anúncio 1% a 5% | vários | 2026 | BR |
| GMV por hora de LIVE "mínimo" de R$ 300 | 1GDosmkdolA (agência) | 2026-08-11 | BR |
| Permanência na LIVE de 3 a 5 s (até 30 s nas melhores) | z-Nq9_kLbQ8 | 2025-11-25 | BR |
| Métricas-bússola de vídeo: tempo médio ≥10 s; conclusão ≥2%; 1 venda a cada 3.000 views | atARj0cZmv8 | 2026-06-28 | BR |
| ROI de GMV Max em beleza de 1,5 a 4 | 1S-Sf8v8ZfY (agência) | 2026-03-22 | EUA |
| Taxa de acerto de vídeo ≈ 5%, "unicórnios" 2% | lPyPPcYjR64 (agência) | 2025-11-15 | EUA |
| CPV de 15% a 20% da receita para escalar | SfAst91eRQc (ferramenta) | 2026-02-13 | EUA |

### 3.4 Circulam sem fonte (não usar)

- Conversão de LIVE de 7,8% e tempo médio de 22 min (ausentes da página citada) [met §4.4].
- GPM "ideal" de LIVE de US$ 50 a 150 (FAQ de ferramenta) [ferr §4].
- "40% ou 60% do GMV vem de LIVE" (LinkedIn; uma agência dos EUA) [live §4; ferr A41].
- "81% dos itens custam menos de US$ 30" (o 81% conhecido é de recompra) [mix A36].
- "Afiliados = 42% do GMV dos EUA" [marca A20].
- Devolução média de 8% a 15% (blog dos EUA) [rep §4].
- "TikTok banca 20% do preço", "ticket médio de R$ 47", "3º maior marketplace", "12º ou 14º país" [dados §6].

---

## 4. Divergências e como medir

| Tema | Lado A | Lado B | Estado | Como medir |
|---|---|---|---|---|
| Meta de lançamento do GMV Max | Meta baixa (0,1 a 1) ou entrega máxima para comprar dado (praticantes EUA; oficial para partida a frio) | 1,5× a 2× o equilíbrio desde o 1º dia (Reiter) | Aberta; nenhum lado mostra comparação | Produtos de margem parecida em campanhas separadas por 14 dias; comparar GMV total da loja (não o ROI do painel) e lucro depois de comissão |
| Produtos por campanha | Poucos e do mesmo comprador (praticantes) | Todos os produtos (oficial) | Aberta | Alternar estrutura por janelas de 2 semanas e medir GMV total e custo por pedido incremental |
| Vídeo de ROI baixo | Excluir (praticantes) | Não remover só porque gasta muito (oficial) | Aberta | Holdout de criativos: excluir metade dos de ROI baixo e comparar receita bruta da campanha |
| O que o ROI desconta | Já desconta tarifa e comissão (praticante BR) | Padrão é bruto; "Pro" em teste (blog oficial) | Leitura mais segura: bruto, salvo modo Pro visível no painel | Conferir a definição na lupa do painel; refazer a conta com pedidos exportados |
| Viral orgânico com GMV Max ligado | Pausar o GMV Max (praticante EUA) | Manter (orientação oficial citada) | Aberta | Teste de pausa (switchback) de poucos dias; olhar se o GMV total cai |
| Separar GMV Max de orgânico | O painel separa (podcast BR) | Não dá (praticante EUA) | Oficial: tudo do produto promovido é atribuído | Usar os seis cortes da Visão geral do Data Compass |
| Redução de comissão | Só 30 dias depois (kid=2850789359355649; kid=5955311610251025) | Edição de convite vale no dia seguinte (kid=6580476438529809) | Hipótese: 30 dias na aberta, dia seguinte no convite; nenhuma página declara | Reduzir uma taxa e ler a data efetiva no extrato |
| Base da comissão com cupom | Inclui o subsídio da plataforma (oficial, 2026-07-01) | Só o valor pago (vídeo de afiliado, 2026-06-22) | Vale a oficial, posterior | Pedido com cupom da plataforma e conferência da comissão no demonstrativo |
| Isenção de loja nova | Só a comissão % (praticante) | Comissão % e taxa fixa (outro praticante) | Página fala só em "taxa de comissão" | Extrato de Finanças nos primeiros 60 dias |
| "Por item" na tarifa | Por unidade (sugere o exemplo) | Por anúncio ou kit | Sem fonte | Extrato de um pedido com 2 unidades do mesmo SKU e de um kit |
| Repasse | 7/3/31 dias (Política de Pagamentos) | Até 35 a 40 dias (Termos) | Provável teto contratual × prazo operacional | Data de liquidação no extrato |
| Devolução de alimento | Não retornável, só reembolso em 72 h (kid=2578485181925121, 2026-04) | Volta lacrado (kid=894339073115921, 2026-09) | A mais recente é a segunda; CDC não tem exceção por categoria | Ler o fluxo no Seller Center para a categoria; checagem jurídica |
| Suplemento por convite | Sim (kid=6907568440706832, 2025-12) | Não listado (kid=6504327061473040, 2026-04) | Divergência entre páginas oficiais | Tentar a qualificação no Centro de qualificação |
| Cancelamento automático | 6 dias úteis (política) | "Hoje é três" (Always Fit) | Vale a política; podem medir coisas diferentes | Conferir o status de um pedido atrasado |
| Pontos do AHR por 300 pedidos | +1 ponto | Não dito (só o teto de 200) | Parcial | Ler o painel de integridade da conta |
| Mix de criativo | Volume (muitos vídeos e ângulos) | 2 a 3 vídeos comem a verba; vence CPM baixo | Ambos podem valer: volume alimenta, poucos vencem | Distribuição de gasto e receita por criativo na Central de Criativos |
| Amostra | Em massa ("o que viraliza paga a conta"; Always Fit no início) | Seleção manual (agências EUA; Always Fit hoje) | Custos diferentes | Custo por amostra que virou conteúdo e GMV por amostra, por coorte |
| LIVE própria | Investir (Natura, Nevo, Neuro) | Deixar para afiliados ou pausar (fabricante BR, marca de moda BR) | Depende de produto e de conflito com afiliados | GMV por hora contra custo por hora, e GMV dos afiliados nas semanas com e sem LIVE da marca |
| Busca ou descoberta | "Não é busca" | "Virou buscador" | Sem divisão pública | Análise de aba Loja e busca no Seller Center (existência no BR não confirmada) |
| Violação reduz alcance | Sim (relato EUA) | Só se o aviso disser (relato de fala do TikTok BR) | Página: medidas de marco "podem reduzir o tráfego" | Impressões antes e depois de uma medida, com controle de sazonalidade |
| Comissão aceitável | 8% a 10% (BR) | 15% a 20% (EUA) | Tabela oficial BR: 8% padrão na maioria | Taxa de aceite de convites e de postagem por faixa de comissão |
| Halo para outros canais | Justifica prejuízo no TikTok (cases EUA) | Sem holdout publicado | Nenhum teste no BR | Geo-experimento ou pausa com dado próprio de site e marketplaces; relatório de transbordamento (método não publicado) |

**Desenhos de teste que as fontes citam** [met §6.3]: holdout de produto ou de criativo; pausa (switchback); cupom só para metade da base; Conversion Lift e geo-experimento (2 a 4 semanas mais 1 a 3 de pós-período); comissão de anúncio menor que a orgânica. Ruído a controlar: sazonalidade, mudança de CPM e datas de campanha produzem o mesmo padrão que canibalização.

---

## 5. Indústria/marca própria × revenda

| Alavanca | Favorece | Por quê | Fonte |
|---|---|---|---|
| LIVE Flash Sale | Quem tem conta oficial (qualquer loja); na prática, a marca | Só a conta oficial cria; o afiliado depende da Flash Sale de criador configurada pelo vendedor | [live A2; kid=5696139560355601] |
| Super Brand Day, campanha de marca, "Brand Crazy Deals" | Marca | Por convite; casos BR são de marca (Granado, Riachuelo) | [marca §2.2; pre §2.6] |
| Comunidade de afiliados e amostra em escala | Marca com margem | Amostra é 100% do vendedor; a margem de fábrica paga amostra, comissão e Ads | [afil §7; cases §3.1] |
| SKU exclusivo do canal, kit, lançamento primeiro no TikTok | Marca | Dá ao afiliado algo "único" para falar e evita comparação direta de preço | [alim §3.1; mix §3.5] |
| Controle de alegação e briefing | Marca | Responde pelo rótulo e pelo que o criador diz; revisão por patamar de views | [vid §3.7; reg §7] |
| Recompra fora da plataforma | Marca de consumível | Leva o cliente para WhatsApp, site, cashback; o TikTok entra como aquisição | [alim A31] |
| Garimpo de produto em alta | Revenda e afiliado | Ferramenta N5 em janela de 7 dias; troca rápida de produto | [ferr §7; mix §7] |
| Comissão como leilão | Revenda e afiliado | O afiliado escolhe pela maior comissão e pelo preço | [afil §7] |
| Preço no mesmo produto | Contra a revenda | Selo de risco "mais caro que os outros" na vitrine; o mesmo SKU em várias lojas | [rank A4] |
| Dropshipping e importação sem estoque | Proibido | Pedido sai do armazém cadastrado; logística internacional vedada | [log A19] |
| Propriedade intelectual | Contra a revenda | Marca de terceiro sem permissão, "inspirado em", "tipo Stanley" derrubam produto | [marca A6; rank §2.7] |
| Categoria por convite | Marca com histórico e documentação | Qualificação pede AHR >150 e SPS >4; marcas convidadas desde o lançamento | [onb A9; alim §5.1] |
| Teto de loja nova e qualificação | Os dois | Tratam revendedor e marca da mesma forma; diferencia quem prova origem e aguenta pico | [onb §7] |
| Tarifa fixa por item | Contra o ticket baixo | 32% do preço a R$ 25; terreno típico da revenda de importado barato | [dados §7] |

**Leitura.** Os números mais altos e com mais fontes do BR são de marca (release oficial e fundador). O lado de revenda aparece quase só em fontes que vendem mentoria. A plataforma reserva à conta oficial e ao convite os formatos de maior alcance comercial. A revenda compete por afiliado e preço, sob o risco de PI e de ruptura do fornecedor [cases §7; marca §7].

**Risco típico de cada lado** [met §9]
- **Revenda:** fim do viral, ruptura de fornecedor, anúncio duplicado entre lojas, violação de termos, link do afiliado que morre quando o estoque acaba.
- **Marca:** canibalização com outros canais, dependência de poucos criadores, alegação em conteúdo de terceiros, conflito com distribuidor e varejo, categoria por convite.

---

## 6. Alimentos e café

### 6.1 Regras da plataforma

- **Porta de entrada:** Produtos Alimentícios (petiscos, laticínios, instantâneos, frescos e congelados, bebidas não alcoólicas, confeitaria) é categoria **só para convidados**; listagem de não qualificado é rejeitada [OFICIAL] kid=6504327061473040, 2026-04-30.
- **Qualificação:** pedido no Centro de qualificação (6 etapas, só desktop, com recurso); para ter e manter, AHR acima de 150 e SPS acima de 4, também nas lojas associadas [OFICIAL] kid=6911810440005392; kid=7734094290093831, 2026-09-29. O formulário "de 4 etapas" com análise de cadastro, citado por praticante, não aparece na página [alim §11 A7].
- **Problema de lógica não resolvido:** o SPS só existe com 30 pedidos em 60 dias, então uma loja só de alimentos sem histórico não teria SPS para cumprir o critério. Hipóteses: o convite dispensa; a loja precisa vender outra categoria antes; o critério vale só para manter [OBS] [onb §5].
- **Proibidos mesmo com convite:** perecíveis, temperatura controlada, caseiros, aditivos, álcool, alimento infantil; exceção para embalado e bebida não alcoólica de quem cumpre a regulação [OFICIAL] kid=6483182812481296, 2026-08-17. Café torrado embalado não está entre os proibidos; cold brew refrigerado cairia em "temperatura controlada"; microtorrefação sem regularização pode ser lida como "caseiro" (a política não define) [OBS] [alim §2.1].
- **Alegações (§4.2):** proibido atribuir propriedade medicinal ou dizer que previne, trata ou cura; "superalimento", "desintoxicação" e "bem-estar" exigem documentação de profissional de saúde; redução de risco só com documento de órgão de saúde; HFSS sem incentivo a excesso nem foco em menor, com advertência se a lei exigir e declaração ao TikTok Shop [OFICIAL] kid=1413208980588305 [alim §10 A4, A5].
- **Passa:** efeito do ingrediente (não do produto), o que está impresso na embalagem, adequação a público, "contém cafeína", "100% arábica", selo ABIC se estiver na embalagem [OFICIAL] kid=3537527768876817; kid=1047177460221712 [rep §5].
- **Peso:** "café emagrecedor" ou termogênico cai em duas proibições: produto para peso e alegação de controle de peso [OFICIAL] [reg §5].
- **Conteúdo de marca:** alimento não está na lista de proibidos; energéticos são restritos; vitaminas não permitidas no BR. Bebida com cafeína em dose de energético merece checagem [OFICIAL; OBS] [vid §5].
- **Devolução:** alimentos e bebidas voltam só lacrados (página de 2026-09-24); outra página (2026-04-14) diz que não são retornáveis e que o reembolso se decide em 72 h [OFICIAL, divergente]. O reembolso sem devolução até R$ 25 favorece o comprador no ticket baixo [rep §5].
- **Validade e embalagem:** o produto precisa ter vida útil suficiente para uso (kid=8322087832667905, 2026-09-08); não há prazo mínimo numérico no BR (os 90 a 270 dias são dos EUA) [OFICIAL]. "Conjuntos de chá e café", copos, chaleiras e jarros estão na governança especial de dano; café em grão ou moído não está [OFICIAL] kid=4836025494996752.
- **Tarifa:** igual para todas as categorias; comissão padrão de colaboração aberta em Alimentos e bebidas de 8% [OFICIAL] kid=24428156307201; kid=3355295847515925.

### 6.2 Regulatório

- **Via sanitária do café:** item 5 do Anexo III da IN 281/2024 (café, cevada, chás, erva-mate, especiarias), que pede comunicação de início de fabricação à vigilância local. A RDC 843/2024 diz que a comunicação não torna o produto aprovado [N2, DOU lido] [alim §11 A37]. **Nenhuma página do TikTok Shop BR pede esse comprovante.**
- **Rótulo do café:** Portaria SDA 570/2022, art. 41 (grupo, espécie, "café" mais marca, lote, CNPJ, endereço, ponto de torra), com veto a função terapêutica não autorizada [N2, lido pela pesquisa do ML] [ML CONSOLIDADO §6.2].
- **Lupa frontal:** RDC 429/2020 e IN 75/2020 são o equivalente BR mais próximo do HFSS; cappuccino ou achocolatado com açúcar podem ter lupa; café puro, em geral, não [OBS, não lido] [alim §2.4].
- **CONAR 2026:** identificação clara e imediata, com marcação nativa e #publi; comissão por desempenho é publicidade; anunciante e agência orientam o criador [N2 via imprensa] [reg A21].
- **Fiscalização:** a Anvisa já agiu em marketplace (ML em Cajamar; Shopee em cosméticos); nada achado contra o TikTok Shop [N2 via imprensa] [reg §2.6].
- **Amostra de alimento:** NF com CFOP 5911/6911; base do ICMS zero para MEI e Simples quando o item é comercializável [OFICIAL] kid=1487157475673872, pode estar superada.

### 6.3 Economia unitária no ticket baixo

| Formato (hipótese de preço) | Plataforma (tarifa + SFP) | % do preço | + afiliado de 8% | + afiliado de 15% |
|---|---|---|---|---|
| Pacote de R$ 25 | R$ 8,00 | 32,0% | 40,0% | 47,0% |
| Pacote de R$ 35 | R$ 9,60 | 27,4% | 35,4% | 42,4% |
| Kit de R$ 65 | R$ 13,80 | 21,2% | 29,2% | 36,2% |
| Kit de R$ 90 | R$ 16,80 | 18,7% | 26,7% | 33,7% |

[OBS, cálculo sobre kid=24428156307201 e kid=5665577566734097]

- **A amostra pesa mais no alimento:** o frete da amostra não cai com o preço. No exemplo hipotético das notas, CPV de R$ 12 e frete de R$ 15 fazem a amostra de um item de R$ 35 custar 77% do preço [OBS] [alim §5.2].
- **Ciclo mais longo:** amostra → conteúdo → venda leva de 4 a 8 semanas; mais cerca de 2 semanas até o algoritmo pegar [OFICIAL, fala, EUA] tGotPuBPS08.
- **Escada de margem do alimento no canal:** preço líquido − tarifa e SFP − comissão de afiliado − amostra − Ads − perdas (avaria, vencimento, 6% do SFP não devolvido) [OBS] [alim §5.2].

### 6.4 O que a observação mostra em café

**Indireta (2026-10-15, busca por vídeos)** [OBS, amostra pequena] [obs §Padrões]
- A venda passa por afiliados: Café Italle em 6 ou mais perfis, Varanda de Vó em 2 ou mais.
- Formato mais citado: 1 kg ou kit; 250 g raro.
- Legendas falam de preço ("preço de café comum", oferta do dia) e selo (100% arábica, gourmet, ABIC); origem quase nunca.
- Café especial em conta própria, com poucos afiliados, teve 5 curtidas no card (correlação, não causa).
- Acessórios de café aparecem mais na busca que o café.

**Direta na vitrine pública (2026-10-16, categoria Alimentos e bebidas > Bebidas > Café, 50 cards e 3 páginas de produto, sessão logada)** [OBS] [obs §Observação direta]
- A categoria Café existe e tem vendedores convidados operando: cápsulas (Dolce Gusto, Delta Q, compatíveis Nespresso), solúvel, "café funcional" (SuperCoffee, Brainstorm), grãos e moído, e **torrefações pequenas de café especial** (Coffee Mais, Minas Estate, América Oro, Fazenda Santa Alcina, Mezzanotte, Grassy, Bry, Tiger/Unique).
- Preço riscado é a regra, com descontos de 15% a 76% (vários perto de −40% a −50%); flash sale com contador em 9 de 50 cards.
- Café em grãos de 1 kg entre R$ 45,99 e R$ 110,00; 250 g de especial entre R$ 16,45 e R$ 24,10 (R$ 66 a 96 por kg); 500 g entre R$ 31,99 e R$ 46,90.
- "Vendidos" do card e da página divergem (61 no card, 5,1 mil na página do mesmo produto): o card parece mostrar vendas recentes.
- Poucas avaliações para o volume (5,1 mil vendidos com 9 avaliações); notas de 4,8 a 5,0.
- Frete grátis e frete pago pelo comprador convivem (um 1 kg com frete a partir de R$ 7,31).
- Uma avaliação cita compra "em live" (kit de 6); lojas de torrefação oferecem kits de 3 e 6 pacotes e kit degustação em drip.
- Itens fora de café aparecem na categoria (semente de pastagem, um livro): a categorização é do vendedor.
- **Limites:** uma passada, um horário, sessão logada (pode haver personalização), sem busca por termo na web.

### 6.5 Demanda, recorrência e casos

- **Demanda declarada baixa:** 11% dos compradores do TikTok Shop compraram alimentos e bebidas, a menor fatia da lista [DADO, Opinion Box]. Não há GMV público de alimentos no BR [alim A16].
- **Marcas convidadas:** BIS (Mondelēz, loja oficial em 2025-07), SEDE (bebida funcional, LIVE de estreia em 2026-07-31), Desinchá, Guday e Power Focus no lançamento; nenhuma divulgou número [OFICIAL via imprensa] [alim A12, A13].
- **EUA (não vale como regra BR):** snacks ≈60% e bebidas ≈26% da categoria; café "cresce muito rápido"; comissão padrão ≈15%; 74% da receita das melhores marcas de mercearia via afiliado; validade mínima e assinatura por produto [OFICIAL, fala; via terceiro] [alim §1].
- **Recompra:** nenhuma fonte mede recompra dentro do TikTok Shop. Marcas de consumível dizem construí-la fora (WhatsApp, SMS, e-mail, cashback, assinatura de cupons a R$ 9,90/mês) [CASE] [alim A31; cases §5].
- **Fora do BR:** Sugarplum (Irlanda) foi de 100 para 3.000 barras/dia com uma tendência; Horns (EUA) fez conteúdo de "fome noturna" ao ver vendas depois das 20 h; alimento fresco é vendável no Reino Unido desde 2024 (proibido no BR) [CASE] [alim §5.5].

### 6.6 Oportunidades estruturais que as fontes apontam (sem recomendação)

- Categoria fechada por convite, com pouca concorrência declarada e demanda ainda pequena (11% dos compradores).
- Prateleira de café com marcas grandes de cápsula e solúvel ao lado de torrefações pequenas de especial.
- Afiliados como canal dominante de venda observada, com espaço para kits e formatos de maior ticket que diluem a tarifa fixa.
- Formatos reservados à conta oficial (LIVE Flash Sale) e conteúdo de origem e preparo pouco explorados nas legendas observadas.
- Ciclo de amostra longo e custo de amostra alto como barreira de entrada para quem não tem margem.
- Regras de alegação estreitas, que deixam espaço para sensorial, ritual, ocasião de uso, preço e rendimento.

---

## 7. TikTok Shop × Mercado Livre × Shopee

Comparação de lógica de venda. Os dados de ML e Shopee vêm dos respectivos `CONSOLIDADO.md` e só servem aqui como contraste.

| Dimensão | TikTok Shop | Mercado Livre | Shopee |
|---|---|---|---|
| Unidade de análise | Produto × criador × peça (vídeo ou LIVE) × superfície | Anúncio × palavra-chave; catálogo com buy box | Anúncio contra anúncio, sem catálogo compartilhado |
| Origem da demanda | Descoberta no feed e na LIVE; a compra fecha muito na aba Loja (≈50% do GMV atribuído em ago/2025) | Busca e catálogo | Busca, descoberta e datas duplas |
| Quem decide a exposição | Conteúdo que converte, afiliados, GMV Max, selos; sem fórmula pública | Reputação (cor), experiência de compra (0 a 100), Full, preço total no catálogo, qualidade do anúncio, Ads em slots fixos | Vendedor Indicado, pontos de penalidade, conversão do anúncio, ROAS-alvo |
| Tarifa | 10% + R$ 4 (<R$ 50) ou 6% + R$ 6 (≥R$ 50), contínua em R$ 50, mais SFP de 6% (teto R$ 50) | Clássico 10–14% ou Premium 15–19% (café 14% e 19%), mais envio em toda venda por peso e faixa | 20% + R$ 4,50 até R$ 79,99; 14% + R$ 16 a R$ 26 a partir de R$ 80 (degrau forte em R$ 80) |
| Custo a R$ 40 [OBS] | 26% (34% com afiliado de 8%) | ≈31% no Clássico, com envio de 0,3–0,5 kg (R$ 6,95) | ≈31% (20% + R$ 4,50) |
| Custo variável que não existe nos outros | Comissão de afiliado (padrão 8%) e amostra 100% do vendedor | Custos do Full (armazenagem, estoque antigo) | Campanhas de Destaque: 3,5% sobre todas as vendas da loja |
| Frete grátis | Selo do SFP pago pelo vendedor (6%); cupons pagos pela plataforma por nível do comprador | Grátis padrão pago pelo ML de R$ 19 a 78,99; rápido pago pelo vendedor a partir de R$ 79 | Para todos, com subsídio limitado (R$ 20/30/40) |
| Logística | Sem fulfillment; Envio pelo TikTok com transportadora designada; teto de pedidos da loja nova | Full decide viabilidade (validade >90 dias para alimentos) e exposição; em café, 83–92% do topo da busca é Full Super | Full com mínimos por item e taxa excepcional abaixo de R$ 20 |
| Ads | GMV Max obrigatório para vender por anúncio e para entrar em campanha; atribui a si orgânico e afiliado | Product Ads por ROAS objetivo (1× a 35×), cobrança por clique; Brand Ads para marca | GMV Max com meta de ROAS; oCPM em parte dos formatos |
| Saúde da conta | SPS (relativo à categoria, 5 métricas) + AHR (pontos 0 a 1.000) | Reputação por cor com limites fixos; MercadoLíder | Pontos trimestrais com −5% a −30% de visibilidade e taxa em dinheiro |
| Preço e paridade | Preço-limite de campanha pode usar plataformas externas; piso de 14 dias na LIVE Flash Sale; preço exclusivo por canal dentro do app | Price matching e preço de referência com concorrentes internos e externos | Desconto enganoso e spam de preço são infração |
| Marca × revenda | Formatos de maior alcance na conta oficial e por convite; afiliados como força de vendas da marca | Buy box favorece revenda eficiente; loja oficial e Brand Ads exigem INPI | Loja Oficial por convite libera Display; revenda forte em ferramentas nativas de promoção |
| Alimentos | Categoria por convite; perecível proibido; alegação de saúde travada; sem validade mínima numérica | Full exige validade, rótulo em português e registro; Supermercado com lista restrita | Atributo Anvisa obrigatório em anúncios novos de 169 categorias; validade e lote visíveis no Full |
| Recorrência | Sem assinatura no BR; CRM no chat do Shop; recompra levada para fora | Sem assinatura de produto; MELI+ não cobre Supermercado | Sem assinatura; cupons e moedas |
| O que é próprio do TikTok | Prova social no vídeo e no criador, não na página; ciclo amostra → vídeo de 4 a 8 semanas; LIVE com preço exclusivo | — | — |

**O que muda na lógica de venda** [OBS, síntese]
1. **O vendedor não espera o comprador; produz o motivo da compra.** No ML e na Shopee, a disputa é por posição numa busca que já existe. No TikTok, o produto precisa de peças de conteúdo e de criadores que o levem ao feed. Sem vídeo no "pool", nem o GMV Max gasta.
2. **O canal de venda é de terceiros.** A maior parte do GMV dos líderes passa por afiliados, com comissão, amostra e gestão de comunidade como custo e como trabalho. Isso não tem equivalente nos dois marketplaces.
3. **A atribuição é mais sobreposta.** O GMV Max atribui a si o orgânico e o afiliado; a medição de incrementalidade é ainda mais difícil que no Product Ads do ML.
4. **A escala esbarra na operação antes da demanda.** Teto de pedidos da loja nova, OVL e cancelamento automático punem o pico viral de um jeito que a busca não produz.
5. **A estrutura de custo favorece kit e ticket médio.** A tarifa contínua em R$ 50 é mais leve que o degrau da Shopee em R$ 80, mas a parte fixa por item e a comissão de afiliado empurram para kits e formatos maiores.
6. **Em alimentos, o TikTok fecha a porta antes; o ML e a Shopee filtram depois** (Full, atributo Anvisa, validade). No TikTok, o convite e a qualificação vêm antes de qualquer venda.

---

## 8. Perguntas abertas para a fase de estratégia

**Regra oficial a confirmar (Seller Center logado ou página que só renderiza com JavaScript)**
1. A tarifa fixa "por item" incide por unidade, por SKU ou por kit? (extrato de Finanças) [pre A25]
2. A isenção de 0% da loja nova cobre a taxa fixa e o SFP? [pre A4]
3. Como uma loja nova de alimentos cumpre "SPS acima de 4" se o SPS só existe depois de 30 pedidos em 60 dias? [onb §5]
4. Quais documentos e prazos o Centro de qualificação pede para Alimentos e bebidas, e por subcategoria (café, snacks, bebidas)? [alim §9]
5. Proteção de ROI, GMV Max Pro e taxa de comissão de Shop Ads: quais limiares e recursos valem no BR (painel de Anúncios da loja)? [ads §9]
6. Na campanha da plataforma, qual ROI a plataforma usa quando cria o anúncio por CPV, campanha a campanha? [pre §11 A35]
7. Redução de comissão: 30 dias ou dia seguinte, por tipo de colaboração? [afil A3, A4]
8. Repasse: 7/3/31 dias ou até 35 a 40? [reg A10, A11]
9. Devolução de alimento: "não retornável" ou "lacrado"? Como o fluxo aparece para a categoria? [rep R12]
10. Teto de outreach de convites no BR por faixa de GMV de afiliados [ferr A16]
11. Regulamento e divisão de custo da Black Friday 2026 [pre A19]
12. Requisitos e custo do Super Brand Day no BR [marca §9]

**Dado que falta para dimensionar**
13. GMV da categoria Alimentos e bebidas e de café no BR (Momentum Works pago; Kalodata ou FastMoss com filtro Brasil) [dados §9]
14. Mix de GMV por superfície (aba Loja × vídeo × LIVE) no BR em 2026 [rank §9]
15. Mix de conta própria × afiliado × Ads no BR [marca §9]
16. Taxa de recompra dentro do TikTok Shop, BR ou fora [alim §9]
17. Benchmarks BR de CTR, CTOR, GPM, conversão de LIVE e custo por pedido do GMV Max, com amostra [met §10]
18. Distribuição de SPS e benchmarks por categoria (limites de nota 1 e 4) para alimentos [rep §9]
19. Taxa de devolução e cancelamento do TikTok Shop BR, para passar de GMV a receita líquida [dados §9]

**Perguntas de desenho (sem resposta nas fontes)**
20. Que parte do GMV atribuído ao GMV Max e ao afiliado é incremental? Nenhum teste publicado no BR; quais desenhos (holdout, pausa, geo) são viáveis com dado de 1ª parte? [met §6]
21. Que proporção de conteúdo próprio × afiliado sustenta alcance orgânico numa categoria de demonstrabilidade baixa como café? (a única evidência é dos EUA, em snacks) [marca §3.6]
22. Qual o custo por amostra que virou conteúdo e o GMV por amostra em alimentos no BR, dado o ciclo de 4 a 8 semanas? [afil §3.8]
23. Como o §3.13.1 (vídeo sem fala ou sem demonstração) é aplicado na prática, se rankings mostram vídeos só de produto entre os que mais vendem? [vid §9]
24. Como o preço exclusivo dentro do TikTok (LIVE Flash Sale, Flash Sale de criador, kit) convive com a regra de preço-limite que lê preços de outras plataformas? [pre §5]
25. Qual a capacidade de expedição necessária para absorver um pico de 10× sem cair em OVL, dado que viral e campanha não entram no recurso? [log A8]
26. Que parte do efeito do TikTok aparece em outros canais (site, ML, Shopee, varejo), e como medir isso sem grupo de controle público? [cases §3.4]
27. Quais alegações de café passam no §4.2 e no CONAR e ainda geram demonstração convincente em vídeo? [alim §2.3; reg §5]

---

## 9. Índice de arquivos

Todos dentro de `pesquisa-marketplaces/tiktokshop/`.

| Arquivo | O que tem |
|---|---|
| `CONSOLIDADO.md` | Este mapa |
| `metodo.md` | Estado da arte de pesquisa e diagnóstico do TikTok Shop: camadas de dado, métricas, auditoria, incrementalidade, revenda × marca |
| `protocolo.md` | Protocolo da pesquisa (níveis N1 a N8, confiança A/B/C, regras) |
| `ads/notas.md` | GMV Max, proteção de ROI, metas, orçamento, criativo, comissão de anúncio, incrementalidade |
| `preco-promocao/notas.md` | Tarifa, SFP, take rate, camadas de preço, preço-limite, cofinanciamento, calendário |
| `logistica-estoque/notas.md` | Modelos de envio, SLA, LDR, SFCR, OVL, devolução, pico viral, transportadoras |
| `ranqueamento-vitrine/notas.md` | Superfícies, vitrine do criador, qualidade de anúncio (EUA), SEO de produto, políticas punidas |
| `produto-mix/notas.md` | Seleção de produto, ferramentas, pico × demanda, sortimento, categorias restritas |
| `reputacao-atendimento/notas.md` | SPS, AHR, metas operacionais, chat, avaliações, pós-venda |
| `alimentos-marca-propria/notas.md` | Categoria por convite, proibidos, alegações, Anvisa e CONAR, café, recompra, cases de alimento |
| `cases-grandes/notas.md` | Always Fit, Natura, Moderna, BigHome, Granado, cases dos EUA, padrões dos líderes |
| `conteudo-video/notas.md` | Política de Conteúdo BR, roteiro, volume, métricas de criativo, reaproveitamento |
| `live-commerce/notas.md` | LIVE Flash Sale, regras de LIVE, roteiro, equipe, mega LIVE, métricas |
| `afiliados-criadores/notas.md` | Colaborações, comissão, amostras, CHR, recrutamento, retenção, agências, tributação do criador |
| `conta-onboarding/notas.md` | Cadastro, loja nova, incentivos, contas, categorias, ERPs, primeiros 90 dias |
| `conta-de-marca-conteudo/notas.md` | Papel da conta oficial, Super Brand Day, pessoas da empresa como criadoras, divulgação |
| `dados-mercado-br/notas.md` | Tamanho, linha do tempo, comparação com ML e Shopee, comprador, mitos de número |
| `ferramentas-analise/notas.md` | Kalodata, FastMoss, EchoTik, Tabcut, Cruva; Data Compass; fluxo das agências |
| `regulatorio-fiscal/notas.md` | CNPJ, NF-e, tributação do afiliado, CDC, CONAR, sanitário, sorteio, reforma tributária |
| `social/notas.md`; `social/posts.tsv`; `social/tiktok.txt`; `social/transcricoes/` | O que criadores, vendedores e agências ensinam em TikTok e Instagram |
| `observacao/vitrine.md`; `observacao/vitrine.tsv`; `observacao/vitrine-cafe-categoria.tsv` | Observação indireta (vídeos de café) e direta (50 cards e 3 páginas da categoria Café) |
| `verificacao/resultado.tsv` | Verificação pelo navegador, com trecho literal da página oficial |
| `videos.tsv`; `selecionados.tsv`; `ids*.txt`; `consultas-*.tsv` | Vídeos listados e selecionados, consultas de busca |
| `transcricoes/` | 233 transcrições do YouTube (`<id>.txt`) |
| `../mercadolivre/CONSOLIDADO.md`; `../shopee/CONSOLIDADO.md` | Mapas dos outros marketplaces, usados só para a comparação da §7 |
