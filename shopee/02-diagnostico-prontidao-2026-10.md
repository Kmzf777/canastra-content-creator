# Shopee: diagnóstico de prontidão (15/10/2026)

> Operação do zero. Cada achado está no formato das agências:
> **evidência → diagnóstico → risco de não agir → próximo passo.**
> Leitura no Claude in Chrome, **sem login** (nem de vendedor nem de comprador), em 15/10/2026
> à tarde. Nada foi criado ou alterado na Shopee. Números de margem saem de
> `shopee/scripts/precificar_shopee.py` (versão de 15/10/2026), com CMV e imposto de
> `mercadolivre/custos.md`.
>
> Abreviaturas: "edu NNNNN" = `https://seller.shopee.com.br/edu/article/NNNNN`;
> "CONS §x" = `pesquisa-marketplaces/shopee/CONSOLIDADO.md`.

---

## Resumo em seis linhas

1. **Conta: não verificável sem login.** A Central do Vendedor redireciona para a tela de entrada. Só você pode dizer se existe uma conta da Canastra e em que documento (CPF ou CNPJ).
2. **As regras que mudam a conta unitária não mudaram desde a verificação da pesquisa (15/10).** Comissão (edu 18483, atualizada em 01/10), frete grátis (23431), Campanhas de Destaque a 3,5% sobre a loja inteira (18712, atualizada em 22/09), Devolução Fácil a R$ 0,49 por pedido (26700, 17/08) e o campo Anvisa (11602, 16/09) foram relidos hoje.
3. **Achado novo que muda a decisão de devolução:** sem o Devolução Fácil, a devolução é **grátis** para o vendedor, salvo culpa dele (produto errado, faltando, avariado por embalagem ruim). Nesse caso a Shopee desconta o frete inteiro, mais R$ 15 se você quiser o produto de volta (edu 23740, 01/07/2026).
4. **A prateleira tem dois blocos de preço e um vão no meio.** "café em grãos 1kg": 27 anúncios de 1 kg torrado avulso, mediana **R$ 76,90**, com um bloco gourmet em R$ 60–94 e um bloco especial/importado em R$ 113–147. **17 dos 40** têm selo Indicado e **1** é Loja Oficial (Italle, com Full). "café moído 500g": commodity em R$ 24–45; especial em R$ 50–60 (Patrick Coffees 80 e 84 pontos).
5. **Pela conta da Shopee, o 1 kg só se paga acima de R$ 94,70** (margem CM3 de 10%). Abaixo de R$ 79,99 sobra pouco, e de R$ 80 a 88,69 é zona morta: cobrar mais rende menos. **O 500 g avulso precisa de R$ 50,77** para 10%. O kit 2 × 500 g a R$ 79,99 dá **prejuízo** (CM3 −R$ 0,20). Portanto, a Canastra entra pelo bloco especial, não pelo gourmet.
6. **Não temos como ser Vendedor Indicado antes de 90 dias** (edu 18456: loja com mais de 90 dias, ≥ 30 pedidos em 30 dias e CNPJ). Por isso a 1ª fase roda sem o selo que 17 dos 40 líderes exibem.

---

## 1. Conta

| | |
|---|---|
| **Evidência** | `seller.shopee.com.br` redireciona para `accounts.shopee.com.br/seller/login` (15/10/2026). Não há sessão logada no Chrome desta sessão. |
| **Diagnóstico** | **Não verificável.** Não sei se a conta existe. |
| **Risco de não agir** | Abrir como CPF e migrar depois. O CPF paga +R$ 3 por item depois de 450 pedidos em 90 dias (edu 18484). O Full exige CNPJ no Simples, Real ou Presumido, com certificado do mesmo CNPJ (edu 26370, CONS §1.2), e o Indicado exige CNPJ (edu 18456). |
| **Próximo passo** | Você me diz se a conta existe. Se não existir, a ordem é esta. **Quem executa é você; eu não crio conta nem aceito termos.** (1) Conta Shopee com telefone (o anúncio não aparece sem telefone confirmado, edu 13388) e e-mail da empresa. (2) Cadastro de vendedor **em CNPJ**, com razão social, endereço de coleta da torrefação em Uberlândia e conta bancária PJ do mesmo CNPJ (edu 13388). (3) Certificado digital e-CNPJ, que só o Full exige, mas convém ter desde o início. (4) Nome e logo da loja. **Limite:** até 5 contas por CNPJ, apenas em categorias diferentes (edu 16310), então uma loja só. |

## 2. Regras que mudam a conta unitária (relidas em 15/10/2026)

| Regra | Valor | Fonte e data | Mudou desde a pesquisa? |
|---|---|---|---|
| Comissão + taxa fixa **por item** | até R$ 79,99: 20% + R$ 4,50 · R$ 80–99,99: 14% + R$ 16 · R$ 100–199,99: 14% + R$ 20 · R$ 200+: 14% + R$ 26. Cobrada só sobre o valor do produto; não incide em cancelamento nem em devolução com retorno | edu 18483, "última atualização 01/10/2026"; a tabela é imagem, conferida pela verificação de 15/10 (CONS §8 item 14) | não |
| Pix | 5% de R$ 80 a 499,99, **pago pela Shopee**; o vendedor recebe o mesmo valor | edu 18483 | não |
| Frete grátis | todos os vendedores; cupom de frete até R$ 20 / 30 / 40 por faixa de preço do item, mais cupom de 50% acima de R$ 10. **Limitado se a loja tiver penalidade ativa** | edu 23431 (16/03/2026) | não |
| Coparticipação de frete | 25% do desconto, teto de R$ 10, **só na logística própria, Intelipost ou API** | edu 25794 (CONS §1.2) | não relido hoje |
| Frete divergente | se o peso ou a medida aferidos forem maiores que o cadastro, a Shopee cobra a diferença em até 90 dias (aba Ajustes do saldo) | edu 4478 (31/10/2025) | novo no repositório |
| Campanhas de Destaque | **3,5% sobre todas as vendas da loja**, além da comissão; só por convite ("vendedores selecionados" pela performance mensal); renovação automática; saída por formulário até 10 dias antes do fim. Benefícios: coleções para afiliados, "Cupons Inteligentes" na loja inteira e atendimento prioritário nos 2 primeiros meses | edu 18712 (atualizado em 22/09/2026) | não |
| Devolução Fácil | R$ 0,49 por pedido confirmado; ativa sozinha quando a loja fica elegível, com 30 dias grátis; **o teste é único** (quem sai durante o teste não volta); só para vendedores integrados; elegibilidade revista mensalmente | edu 26700 (17/08/2026) | não |
| Devolução **sem** o programa | grátis, salvo culpa do vendedor: aí é o frete inteiro, mais R$ 15 se ele quiser o produto de volta | edu 23740 (01/07/2026) | novo no repositório |
| Pontos de penalidade | trimestre; atraso ≥ 5% e não envio ≥ 8% (com ≥ 2 pedidos) = 1 ponto; punição a partir de 3 pontos; multas de R$ 100 a R$ 1.500 não cobradas com VBM abaixo de R$ 2.500 no mês anterior | edu 7955 (CONS §1.3) | não relido hoje |
| Vendedor Indicado | nota ≥ 4,5, chat ≥ 60%, TNE ≤ 2%, ≤ 1 ponto, preparo ≤ 1 dia útil, sábado ≥ 20%, **CNPJ, loja > 90 dias, ≥ 30 pedidos em 30 dias, ≥ 10 compradores únicos** | edu 18456 (CONS §1.3) | não relido hoje |
| Full | CNPJ; preço ≥ R$ 20; 10 un./mês até R$ 79,99 e 5 un./mês a partir de R$ 80; até 30 kg; validade e lote visíveis; ociosidade cobrada desde 01/03/2026 (Supermercado a partir de 2 meses); no-show de R$ 5 e R$ 3 por unidade | edu 26370, 23197, 26581, 27632 (CONS §8 itens 2, 3, 9, 11) | não relido hoje |
| Full+ | −0,5 a −2 p.p. de comissão em itens ≥ R$ 50 com ≥ 40% dos pedidos via Full, até dez/2026 | edu 27600 (CONS §1.1) | não relido hoje |

"Não relido hoje" quer dizer que a verificação da pesquisa leu o artigo nesta mesma data (15/10) e eu não repeti a leitura.

**Pendência que trava parte da conta:** o kit pagar **uma** taxa fixa só não tem fonte oficial (CONS D18). O script assume 1 taxa e mostra o caso de 2 taxas. Isso precisa ser medido no extrato do primeiro pedido de kit.

## 3. Logística de largada

| | |
|---|---|
| **Evidência** | DTS de 2 dias úteis (help 76324, CONS §1.2). A lista de "Envio de Pedidos" do Centro de Educação mostra a Logística do Vendedor (edu 25782, 25794, 26810), a retirada pelo comprador (23547) e as normas de embalagem. **As modalidades disponíveis para o CEP da torrefação (coleta ou ponto de entrega) só aparecem dentro da Central logada.** O Shopee Turbo atende raio de 7 km com entrega em 4 h (edu 27255; CONS §8 item 4). |
| **Diagnóstico** | Com a logística da Shopee, o frete do vendedor é **zero** na conta: o cupom cobre até R$ 30 por item de R$ 80–199,99, e o excedente fica com o comprador. A logística própria custaria até R$ 10 de coparticipação por pedido e derruba o CM3 do 1 kg a R$ 99,99 de R$ 13,50 para R$ 6,00 (script). |
| **Risco de não agir** | Cadastrar o peso sem a embalagem de envio gera cobrança de frete divergente em até 90 dias (edu 4478). Prometer 1 dia de preparo sem rotina de expedição vira atraso, e atraso ≥ 5% vira ponto. |
| **Próximo passo** | (a) Pesar e medir o 1 kg e o 500 g **já na caixa de envio** e cadastrar esses números. (b) Você me diz qual modalidade aparece para o CEP de Uberlândia quando abrir a Central. (c) Alimento: café torrado é, em regra, dispensado de registro na Anvisa, e o campo do anúncio aceita "00" (edu 11602), mas **confirme com o contador ou com o responsável técnico** antes do 1º anúncio. Número inventado remove o anúncio sem aviso. Proibido no título, na descrição, no vídeo e na live: qualquer alegação de saúde (edu 11602 §3). |

## 4. Prateleira de café (observação de 15/10/2026, sem login)

**Método.** Busca em `shopee.com.br`, ordenação `sortBy=sales` (o botão aparece como "Em Destaque"), 1ª página de 40 cards por termo, extração por JavaScript. A sessão estava deslogada. **Sem login, o card não mostra "vendidos"**: a ordem é a da plataforma, mas o volume não foi medido. Os selos vêm da imagem `flag-label`: 48 px = "Indicado", 37 px = "Oficial", 23 px = "Full" (conferido por zoom). Os preços marcados "no Pix" já têm o desconto de 5% (preço de lista ≈ Pix ÷ 0,95).

### 4.1 "café em grãos 1kg"

- **Selos:** Indicado em 17 de 40. Oficial em 1 (Italle, que também tem Full). Full em 2.
- **UF:** MG domina, seguida de SC, SP, PR e GO.
- **1 kg torrado avulso (27 cards):**
  - mínimo R$ 59,90;
  - **mediana R$ 76,90**;
  - Q3 ≈ R$ 126;
  - máximo R$ 147,25 no Pix (Orfeu).
- **Bloco gourmet, R$ 60 a 94 (19 cards):**
  - Italle R$ 76,90 (Oficial + Full);
  - Origem R$ 73,70;
  - Gálatas R$ 69,90;
  - Dimoá R$ 71,93;
  - Café do Professor R$ 69,99 (5 anúncios);
  - Mizael 84 pontos R$ 84,55 (Indicado).
- **Bloco especial/importado, R$ 113 a 147 (8 cards; Bergamasco aparece 2 vezes):**
  - Delta R$ 113,05 Pix;
  - Barão do Rio Branco R$ 126,35 Pix (Indicado);
  - Prima Qualità R$ 128,25 Pix;
  - Bergamasco 82 pontos R$ 129,11 Pix;
  - Lavazza R$ 133,19 Pix;
  - Orfeu R$ 147,25 Pix.
- **Kits e escada:**
  - Loffe 2 × 1 kg R$ 147,16 Pix (R$ 73,58/kg);
  - OliveiraCoffee 2 kg R$ 89,30 (R$ 44,65/kg);
  - Mizael 3 × 1 kg R$ 231,30 Pix (R$ 77,10/kg);
  - Tostati 2 × 1 kg R$ 237,99 Pix (R$ 119/kg).
- **Ruído na busca:** 7 dos 40 são café **cru/verde**.
- **Preço riscado** em cerca de metade dos cards (−5% a −53%).

### 4.2 "café moído 500g"

- **Selos:** Indicado em 19 de 40. Oficial em 4 (Italle × 2, Melitta × 2), dos quais 3 com Full.
- **Commodity, R$ 24 a 45:**
  - Italle R$ 24,49 e R$ 28,46;
  - Pilão R$ 32,90;
  - Melitta R$ 37,99 e R$ 42,90;
  - Odebrecht R$ 24,90 e R$ 39,90.
- **Artesanal de MG, R$ 25 a 36:**
  - Caseiro R$ 25,20;
  - Sítio São Jorge R$ 29,67;
  - Goiabeiras R$ 35,99.
- **Especial, R$ 50 a 60:**
  - Patrick Coffees 80 pontos R$ 50,00;
  - Patrick Coffees 84 pontos R$ 60,00 (R$ 120/kg).
- **Kits de 2 a 5 pacotes** são comuns: Odebrecht 5 × 500 g a R$ 113,91 Pix; "Kit 4 × 500 g" a R$ 79,99, exatamente no degrau.
- **Ruído na busca:** cevada e "café de milho" aparecem na busca de café.

### 4.3 Diagnóstico da prateleira

| | |
|---|---|
| **Evidência** | Acima. |
| **Diagnóstico** | Disputar o bloco gourmet (R$ 60–80/kg) com o CMV da Canastra não fecha: o 1 kg a R$ 79,99 deixa CM3 de R$ 4,80 (6%), com ROAS de equilíbrio de 16,7. O espaço é o **bloco especial**, R$ 99,99 a R$ 129,90/kg, onde quem está são importados (Lavazza, Delta, Orfeu), uma fazenda de SP (Bergamasco) e poucos torrefadores de MG. A diferenciação que a prateleira mostra funcionar é **origem + pontuação + "torrado fresco"** no título (Bergamasco "82 PONTOS", Patrick "84 pontos", Loffe "FRESCA DIRETO DO PRODUTOR"). A Canastra tem as três de verdade: Serra da Canastra, fazenda em Medeiros e torrefação própria em Uberlândia. |
| **Risco de não agir** | Entrar no preço da mediana (R$ 76,90) é trabalhar quase de graça, e com qualquer Ads é trabalhar no prejuízo. |
| **Próximo passo** | Com login de **comprador** no Chrome: ler os "vendidos" e a nota dos cards do bloco especial e abrir 5 anúncios líderes (título, fotos, vídeo, variações, frete). Faltam ainda os termos "café especial", "café torrado e moído" e "café em grãos" nas quatro ordenações. |

## 5. Economia unitária (script, 15/10/2026)

Logística da Shopee, CNPJ, sem cupom; kit = 1 taxa fixa (**não medido**). CM3 = CM1 − Devolução Fácil.

| SKU | preço | R$/kg | comprador no Pix | CM1 | CM3 | CM3 com campanha 3,5% | ROAS de equilíbrio (sem → com campanha) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 kg | 79,99 | 79,99 | 79,99 | 5,29 | 4,80 | 2,00 | 16,7 → 40,0 |
| 1 kg | 99,99 | 99,99 | 94,99 | 13,99 | 13,50 | 10,00 | 7,4 → 10,0 |
| 1 kg | 119,90 | 119,90 | 113,91 | 25,32 | 24,83 | 20,63 | 4,8 → 5,7 |
| 500 g | 49,90 | 99,80 | 49,90 | 4,93 | 4,44 | 2,69 | 11,2 → 18,5 |
| 500 g | 54,90 | 109,80 | 54,90 | 8,48 | 7,99 | 6,07 | 6,9 → 9,0 |
| 500 g | 59,90 | 119,80 | 59,90 | 12,03 | 11,54 | 9,44 | 5,2 → 6,3 |
| Kit 2 × 500 g | 79,99 | 79,99 | 79,99 | 0,29 | −0,20 | −3,00 | sem margem |
| Kit 2 × 500 g | 99,99 | 99,99 | 94,99 | 8,99 | 8,50 | 5,00 | 11,8 → 20,0 |
| Kit 2 × 1 kg | 199,99 | 100,00 | 189,99 | 39,99 | 39,50 | 32,50 | 5,1 → 6,2 |

**Pisos (CM3):**

| SKU | margem zero | 10% | 15% | 20% |
|---|---:|---:|---:|---:|
| 1 kg | R$ 73,19 | R$ 94,70 | R$ 108,78 | R$ 118,31 |
| 500 g | R$ 43,61 | R$ 50,77 | R$ 55,30 | R$ 60,70 |
| Kit 2 × 1 kg | R$ 148,59 | R$ 170,77 | R$ 184,52 | R$ 211,21 |

**Zonas mortas:** 1 kg de R$ 80,00 a R$ 88,69 e de R$ 100,00 a R$ 105,19; kit 2 × 1 kg de R$ 200,00 a R$ 207,78.

**Kit × avulso, 2 × 1 kg:**
- kit a R$ 199,90 com 1 taxa fixa: CM3 R$ 39,43;
- o mesmo kit pagando 2 taxas: R$ 19,43;
- 2 avulsos a R$ 99,99, em 2 pedidos: R$ 27,00.

**A vantagem do kit depende inteiramente do D18** (kit pagar 1 taxa só). Por isso o 1º pedido de kit precisa ser lido no extrato.

**Estresse no 1 kg a R$ 99,99:**

| Cenário | CM3 |
|---|---:|
| Base | R$ 13,50 |
| Campanha 3,5% + Ads com ACOS 8% + cupom de R$ 5 | **−R$ 2,37** |
| Logística própria | R$ 6,00 |

Quem empilhar as alavancas no degrau de R$ 99,99 trabalha no prejuízo.

## 6. Ferramentas de crescimento para loja nova

| Ferramenta | O que se sabe | Fonte | Para nós, no início |
|---|---|---|---|
| Shopee Ads (GMV Max) | Meta de ROAS com 3 sugestões; pré-pago; oCPM só no GMV Max - Anúncios de Produto; atribuição de 7 d por clique (+1 d por impressão no GMV Max) | ads.shopee.com.br/learn/faq/473/1527 e /2205 (CONS §1.4) | Disponível. Orçamento mínimo de R$ 10/dia e recarga mínima de R$ 50 **sem fonte oficial** (CONS §8). ROAS de equilíbrio de 7,4 a R$ 99,99 e de 4,8 a R$ 119,90; com meta alta demais, a Shopee não gasta (CONS §0) |
| Shopee Vídeo e Live | Vídeo de 10–60 s no anúncio (edu 18658); Live existe na Central de Marketing ("Anúncios em Lives") | CONS §1.4 | Disponível. Custo: produção |
| Afiliados | Programa geral pago pela Shopee; "Afiliados do Vendedor" com comissão extra paga pelo vendedor | blog Shopee 16/06/2026 (PRE A32); CONS §2.2 | A comissão extra sai do CM2 (`--afiliado` no script) |
| Cupons | De loja, de seguidor, de produto; 1 cupom do vendedor + 1 da Shopee por compra | help 76177 (CONS §1.1) | Disponível desde o dia 1. Cupom de R$ 5 no 1 kg a R$ 99,99 leva o CM3 de 13,50 a 8,95 |
| Campanhas de Destaque | Só por convite, a partir do desempenho mensal; 3,5% sobre a loja inteira | edu 18712 | **Não vem para loja nova.** Quando o convite vier, é decisão: a R$ 99,99 a campanha come 26% do CM3 |
| Datas duplas | Uma por mês (11.11, 12.12) | blog Shopee 30/09/2026 (CONS §1.1) | Prazos de nomeação **não medidos** |
| Vendedor Indicado | Ver §2 | edu 18456 | Impossível antes de 90 dias e 30 pedidos/mês |
| Full | Ver §2 | edu 26370 e outros | Exige giro mínimo por item e CNPJ; fase 3 |

## 7. O que falta e quem destrava

| # | Falta | Quem | Por quê |
|---|---|---|---|
| 1 | Existe conta? CPF ou CNPJ? | Rafael | Define o passo 1 |
| 2 | Login de **comprador** no Chrome | Rafael | Ler "vendidos", notas e anúncios líderes; terminar a prateleira (§4.3) |
| 3 | Modalidades de envio para o CEP de Uberlândia | Rafael abre a Central; eu leio | Coleta × ponto; prazo real |
| 4 | Código Anvisa do café torrado ("00" se dispensado) | contador ou responsável técnico | O anúncio é removido sem aviso se o código estiver errado |
| 5 | Pontuação SCA e notas por SKU, com laudo | Rafael | É o diferencial que a prateleira premia; não pode ser inventado |
| 6 | Peso e medidas do 1 kg e do 500 g na caixa de envio | expedição | Evita cobrança de frete divergente |
| 7 | Extrato do 1º pedido avulso e do 1º kit | depois da 1ª venda | Mede taxa fixa, kit (D18) e frete real |

## Nota de método

- A busca sem login funcionou **duas vezes seguidas** em 15/10/2026 (o bloqueio de 14/10 não se repetiu), mas sem "vendidos". Não force uma terceira: peça o login de comprador.
- A conexão com o Chrome caiu no meio da leitura e o grupo de abas foi recriado. As abas antigas (`seller.shopee.com.br/edu/...`) podem ter ficado abertas na janela do Chrome, fora do alcance desta sessão.
