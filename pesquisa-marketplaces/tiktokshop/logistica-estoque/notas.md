# Logística, frete e estoque no TikTok Shop: notas do analista

Frente: logistica-estoque · Data: 2026-10-15 · Escopo: Brasil. EUA, Malásia e Reino Unido entram só como comparação e vêm marcados.
Protocolo: `../protocolo.md` v1. Base comum: `../metodo.md` §2.

Convenções:
- Tipos de fonte: [OFICIAL] · [PRÁTICA] · [CASE] · [DADO] · [OBS].
- Páginas da Academy BR aparecem como `kid=` e ficam em `seller-br.tiktok.com/university/essay?knowledge_id=<kid>`. Todas foram lidas em 2026-10-15 sem login, e a data citada é a que a página mostra.
- Vídeos do YouTube aparecem pelo id (transcrição em `../transcricoes/<id>.txt`). Posts do TikTok aparecem pelo id numérico, como em `../social/notas.md`.
- Regra de plataforma anterior a 2026-04-15 leva a marca **(pode estar superada)**.

---

## 1. Resumo executivo

1. **No Brasil não existe fulfillment da plataforma.** O modelo padrão é "Envio pelo TikTok" (Enviado pela Plataforma): o TikTok designa a transportadora e a etiqueta sai da Central do Vendedor. O "Envio pelo Vendedor" existe na política, mas exige transportadora compatível e, na prática, aprovação e TMS. [OFICIAL] kid=1442971111884545, 2026-03-06 (pode estar superada); [DADO] ANYMARKET, 2026-09-15.
2. **Prazos oficiais (Política de Logística, 2026-09-30):**
   - "Pronto para envio" em 1 dia útil;
   - "Em trânsito para envio" (TTS) em 2 dias úteis, com corte às 23:59:59 (UTC-3);
   - sem status "Enviado" em 6 dias úteis, o pedido é cancelado automaticamente.
   [OFICIAL] kid=1444948508280592.
3. **Quatro metas logísticas oficiais.** LDR ≤ 4%, SFCR ≤ 2,5%, rastreamento válido (VTR) ≥ 95% e envio rápido (FDR, em 1 dia útil) recomendado ≥ 90%. [OFICIAL] kid=1444948508280592, 2026-09-30.
4. **O LDR passou a contar pedido atrasado ainda não enviado** desde 2026-03-16. O SFCR usa janela de 7 dias corridos. Pedidos de amostra ficam fora dos dois. [OFICIAL] kid=4263127323510529 (2026-03-10); kid=3321767214286609 (2026-08-26); kid=3333356285478657 (2026-07-14).
5. **A penalidade logística é restrição de vendas, não multa.** O pacote inclui limite de volume de pedidos (OVL), restrição de campanha e dedução do saldo. Com o OVL ativo, o comprador vê o produto como **"Esgotado"**. Não existe "taxa por atraso". [OFICIAL] kid=3309653722089232 (2025-10-27, pode estar superada); [PRÁTICA] 9l6u6uw-85k, 2026-08-24.
6. **Logística entra em três portas:**
   - **SPS:** a nota precisa de 30 pedidos em 60 dias e mede taxa de envio atrasado e cancelamento por culpa do vendedor;
   - **campanhas:** exigem SPS ≥ 3,0, e quem não tem SPS não pode estar penalizado por LDR/SFCR;
   - **frete grátis:** o Programa de Taxas de Envio pode tirar da lista o produto com "má experiência".
   [OFICIAL] kid=7517966208927489; kid=2996214162966289; kid=5665577566734097.
7. **Frete grátis tem custo de 6% sobre o preço**, com teto de R$ 50 por produto. A inscrição é automática e a plataforma subsidia cupons de frete por nível de comprador (ex.: compra mínima de R$ 29, subsídio de até R$ 20). A taxa não volta em devolução de pedido enviado. [OFICIAL] kid=5665577566734097, 2026-08-31.
8. **Quem paga a devolução depende do motivo.** Em "não preciso mais" ou tamanho (moda), paga o TikTok. Em defeito, item errado, faltando, dano com caixa intacta ou atraso, o vendedor paga ida e volta. Até R$ 25 vale reembolso sem devolução, coberto pela plataforma (medida temporária). [OFICIAL] kid=894339073115921, 2026-09-24; kid=5665577566734097.
9. **Loja nova começa com teto de 50 pedidos por dia** (depois 100 e 200, e ilimitado no nível Profissional). Lançar com criador grande nessa fase faz o produto "esgotar" no meio do dia. [OFICIAL] kid=1444948507379472, 2026-04-02 (pode estar superada); [CASE] z-Nq9_kLbQ8.
10. **O caso mais documentado de ruptura por pico é o da Always Fit**, que se apresenta como top 1 do TikTok Shop BR. No 10/10 de 2025 os pedidos passaram de ~1.000 para mais de 10.000 por dia, a logística falhou, veio uma punição com teto de 1.000 pedidos/dia e os sócios estimam perda de R$ 1 a 1,5 milhão. [CASE] z-Nq9_kLbQ8, 2025-11-25; 6sWUmzRywWU, 2026-10-13. Narrativa dos sócios, sem auditoria.
11. **A Política de Envio BR proíbe dropshipping e logística internacional para vendedor brasileiro.** O pedido precisa sair do armazém cadastrado, e produto comprado em outro varejista ou marketplace é proibido. [OFICIAL] kid=1442971111884545, 2026-03-06 (pode estar superada).
12. **Alimentos:**
    - proibidos: perecíveis, itens com temperatura controlada, caseiros (sem exceção), aditivos e vencidos;
    - embalado ou pré-embalado: só para vendedor qualificado (categoria só para convidados);
    - devolução de alimento deve voltar lacrada.
    [OFICIAL] kid=6483182812481296 (2026-08-17); kid=6504327061473040 (2026-04-30); kid=894339073115921.
13. **A transportadora própria ainda não opera.** A TikTok Logistics Brazil (capital de R$ 111 milhões) existe, mas não há data pública de operação nem de CD próprio. As parceiras citadas são J&T Express, Correios e iMile, com Total Express e Jadlog como pontos de postagem. A logística reversa usa agências dos Correios. [DADO] Fast Company Brasil, 2026-08-19; Central do Varejo/Mundo Logística, s/d; ANYMARKET, 2026-09-15.
14. **O mito mais difundido vem dos EUA:** "o seller shipping acabou". O TikTok Shop US suspendeu o prazo de 25/02/2026, e a regra não vale para o Brasil. [OFICIAL via terceiro] ChannelX, 2026-02-18 (EUA). Os vídeos q2QT6vmni2s e L5CnT13a8PI repetem a versão superada.

---

## 2. Como funciona (mecânica e regras oficiais)

### 2.1 Modelos de envio no Brasil
| Modelo | O que é | Situação BR | Fonte |
|---|---|---|---|
| **Envio pelo TikTok** ("Enviado pela Plataforma") | Transportadora (LSP) designada pelo TikTok; etiqueta e rastreio gerados na Central | Padrão. O vendedor não escolhe a transportadora pedido a pedido | [OFICIAL] kid=1442971111884545, 2026-03-06 (pode estar superada); [DADO] ANYMARKET, 2026-09-15 |
| **Envio pelo Vendedor** | O vendedor escolhe um LSP "compatível" e informa o rastreio | Prevista na política. Segundo terceiro, antes valia só para amostras; agora se expande para pedido normal, com aprovação sem critério público e TMS específico | [OFICIAL] kid=1442971111884545; [DADO] ANYMARKET, 2026-09-15 |
| **Fulfillment da plataforma** (equivalente ao FBT dos EUA) | Armazenagem, separação e envio pelo TikTok | **Não disponível.** A plataforma diz que o estoque é do vendedor | [DADO] UpSeller, 2026-08-20; ANYMARKET, 2026-09-15; Central do Varejo, s/d |
| **Transportadora própria** (TikTok Logistics Brazil Ltda.) | Empresa de transporte rodoviário de cargas com capital de R$ 111 mi | Registrada. Os termos de logística de fev/2026 já a citariam como responsável formal. Não opera sozinha: as parceiras continuam | [DADO] Fast Company Brasil, 2026-08-19; UpSeller, 2026-08-20 |

**Saída do pacote (só Envio pelo TikTok).** [OFICIAL] kid=1442971111884545.
- **Drop-off:** o vendedor leva o pacote ao ponto de postagem antes do prazo de TTS.
- **Pick-up:** a transportadora deve coletar em até 48 horas depois de "Organizar envio".
- Segundo terceiros, a coleta no endereço só existe em parte do Sudeste. [DADO] Central do Varejo, s/d; UpSeller, 2026-08-20.
- Para o vendedor, o TTS conta a partir do scan de coleta ou postagem. Se o primeiro scan for de trânsito, a plataforma desconta 12 horas úteis desse scan. [OFICIAL] kid=1444948508280592, 2026-09-30.

**Transportadoras.** Nenhuma página oficial lida traz a lista. A imprensa atribui à página do vendedor J&T Express, Correios e iMile no Enviado pela Plataforma, mais pontos de postagem de Total Express e Jadlog. [DADO] Central do Varejo, s/d; UpSeller, 2026-08-20. O Mundo do Marketing cita JT, Total Express e Jadlog. [DADO] 2026-08-19.

**Ajuste de frete por rota.** A tabela de frete foi ajustada em rotas que saem de SP, RJ, MG e ES, para lojistas do Enviado pela Plataforma. [DADO] Mundo do Marketing, 2026-08-19. Um afiliado repete a informação. [PRÁTICA] 4LnQ0HB6A_Q, 2026-08-21 (vende curso e ferramenta).

**Limites de pacote (Enviado pela Plataforma).** Até 30 kg, maior lado de até 100 cm e soma dos lados de até 200 cm. [DADO] ANYMARKET, 2026-09-15. A política oficial lida só remete aos requisitos do LSP.

**Documentos.** Para emitir a NF-e e enviar, vale o seguinte:
- NF-e autorizada pela SEFAZ antes do envio, com os 8 primeiros dígitos do CNPJ iguais aos da loja. [DADO] ANYMARKET, 2026-09-15;
- DANFE ao lado da etiqueta, nunca sobre o código de barras. [DADO] ANYMARKET, 2026-09-15;
- o produto precisa ter também a natureza de operação de bonificação (CFOP de brinde), senão a nota do pedido de amostra não sai. [PRÁTICA] 9w2ndZKzsIQ, 2026-05-22.

### 2.2 Prazos (SLA) e calendário
- **Pronto para envio (RTS):** 1 dia útil. **TTS/despacho:** 2 dias úteis. Os dois valem igual para Envio pelo TikTok e Envio pelo Vendedor. [OFICIAL] kid=1444948508280592, 2026-09-30. A tabela da página veio truncada na leitura, então os números devem ser conferidos no navegador.
- **Cancelamento automático:** 6 dias úteis sem "Enviado". [OFICIAL] kid=1444948508280592; kid=3321767214286609; kid=894339073115921.
- **Dia útil:** exclui sábado, domingo e feriado nacional. Feriado estadual ou municipal só vale para quem tem armazém naquele estado ou município. Corte às 23:59:59, UTC-3. [OFICIAL] kid=1444948508280592.
- **Versões anteriores:**
  - Vídeo oficial de 2025-05-30: até 3 dias úteis e cancelamento em 7. [OFICIAL] 7510044886742125829 (pode estar superada).
  - Um sócio da Always Fit diz que o cancelamento por atraso "era seis, hoje é três". [CASE] 6sWUmzRywWU, 2026-10-13. **Isso contradiz a política de 2026-09-30, que diz 6 dias úteis.** Os dois podem estar falando de coisas diferentes (dias corridos de atraso depois do SLA × dias úteis desde o pedido). Fica como ponto para checar.
- **Rastreio:**
  - código errado só pode ser corrigido em 72 horas;
  - no Envio pelo Vendedor, rastreio sem movimento em 24 horas é tratado como fraude;
  - se o LSP do vendedor não atualiza o rastreio, a falha conta contra o vendedor.
  [OFICIAL] kid=1442971111884545 (pode estar superada).

### 2.3 Métricas logísticas oficiais (BR)
| Métrica | Definição | Janela | Meta | Exclusões | Fonte |
|---|---|---|---|---|---|
| **LDR** (taxa de envio atrasado) | (enviados com atraso + atrasados ainda não enviados) ÷ pedidos com vencimento no período | "Período aplicável" não definido; aviso usa "últimos 7 dias" | ≤ 4% "em todos os momentos" | Cancelados antes do SLA; amostras grátis | [OFICIAL] kid=3321767214286609, 2026-08-26 |
| **SFCR** (cancelamento por erro do vendedor) | Cancelamentos por erro do vendedor (falta de estoque, preço errado) + cancelamentos automáticos por não envio ÷ pedidos | 7 dias corridos | ≤ 2,5% | Amostras grátis | [OFICIAL] kid=3333356285478657, 2026-07-14 |
| **FDR** (envio rápido) | Envio em até 1 dia útil | não informada | ≥ 90% (recomendação) | — | [OFICIAL] kid=1444948508280592 |
| **VTR** (rastreamento válido) | Rastreio, provedor e serviço corretos | não informada | ≥ 95% | — | [OFICIAL] kid=1444948508280592 |
| Cancelamento por falha do vendedor (no SPS) | Mesma ideia do SFCR | Pedidos pagos em 30 dias | Benchmark por categoria, sem número na página | — | [OFICIAL] kid=7517966208927489, 2026-07-07 |

Mudança de 2026-03-16: o LDR antes contava só pedidos já enviados. [OFICIAL] kid=4263127323510529, 2026-03-10 (pode estar superada, mas a regra se repete em kid=3321767214286609 de agosto). A mesma mudança chegou aos EUA (ou mercado não especificado) em 2026-06-15, com fiscalização a partir de julho e um corte no mesmo dia para pedido criado antes das 14h. [DADO] Common Thread, 2026-06-15. **Não vale para o Brasil.**

### 2.4 Penalidades e recurso
- **Escada no BR:**
  - LDR > 4% gera **advertência**, sem penalidade por si só;
  - LDR "significativamente" acima de 4% gera penalidade: **OVL**, restrição de campanha e outras;
  - SFCR alto gera OVL, restrição de campanha e **dedução do saldo liquidado**;
  - dedução não paga em 30 dias pode levar a OVL ou congelamento de transferências;
  - reincidência agrava as medidas.
  [OFICIAL] kid=3321767214286609; kid=3333356285478657; kid=1444948508280592.
- **O BR não publica faixas numéricas para o OVL.** Na **Malásia**, a faixa de LDR entre 10% e 30% limita a 90% do volume médio diário, entre 30% e 50% a 70%, e acima de 50% a 50%. [DADO] BigSeller, vigência 2024-09-02 (Malásia; pode estar superada). Serve como ordem de grandeza, não como regra BR.
- **OVL:**
  - gatilhos: período de loja nova, LDR ou SFCR altos, "risco operacional" e outros;
  - se mais de uma regra se aplica, vale o menor limite;
  - o limite zera a cada dia do calendário;
  - o comprador vê o produto **"Esgotado"**.
  [OFICIAL] kid=3309653722089232, 2025-10-27 (pode estar superada). Um embaixador do programa descreve a mesma sequência: alerta, depois produto "esgotado durante o dia" mesmo com estoque, depois afeta a integridade da conta e, em caso extremo, suspensão que pode atingir outras contas do mesmo CNPJ. [PRÁTICA] 9l6u6uw-85k, 2026-08-24 (vende treinamento; o trecho do CNPJ não foi confirmado em N1).
- **Recurso de LDR:**
  - antes da penalidade há 24 horas para recorrer; depois, 30 dias, e um segundo recurso em 15 dias;
  - para OVL por SFCR, são 48 horas antes da penalidade.
  [OFICIAL] kid=3321767214286609; kid=3333356285478657.
- **Cenários de recurso aceitos (lista fechada):**
  - falha de coleta da transportadora (não veio, veio fora das 8h às 18h, veículo cheio, scan atrasado);
  - ponto de postagem fechado ou scan atrasado no ponto;
  - feriado municipal fora do calendário;
  - erro de sistema;
  - força maior;
  - pedido do cliente.
  Tudo exige prova com data e hora. **Pico de vendas, viral, campanha e falta de estoque não estão na lista.** [OFICIAL] kid=3026645972993808, 2026-03-06 (pode estar superada).

### 2.5 Logística no SPS, nas campanhas e no frete grátis
- **SPS (BR):**
  - a nota só aparece com 30 pedidos concluídos em 60 dias;
  - acima de 4, a loja está em alto desempenho; acima de 4,5, pode ganhar o selo de loja de qualidade;
  - o SPS influencia campanha, saída do período de loja nova e ciclo de pagamento.
  [OFICIAL] kid=7517966208927489, 2026-07-07. Pesos e lista completa das métricas BR não estão na página (ver §9).
- **Campanhas:**
  - SPS ≥ 3,0 desde abril de 2026;
  - desde agosto de 2026, loja sem SPS não pode estar penalizada por LDR/SFCR;
  - **dois SFCR seguidos em campanha geram período de cancelamento obrigatório na campanha seguinte**;
  - produto com problema de "item ausente/errado e defeituoso" não se qualifica.
  [OFICIAL] kid=2996214162966289, 2026-07-24.
- **Programa de Taxas de Envio (SFP):**
  - 6% do preço, teto de R$ 50 por produto, cobrado só em pedido entregue; pedido cancelado antes do envio não paga;
  - dá selo de "frete grátis" em vídeo, aba Loja e LIVE, e "tráfego gratuito de anúncios" a quem se qualifica;
  - o TikTok pode suspender a participação por atraso excessivo, avaliação negativa constante ou falha de embalagem e etiqueta;
  - produto com "má experiência do cliente" sai da lista de frete grátis, e aí o comprador paga o frete. A página não define "má experiência";
  - o subsídio da plataforma é aplicado antes do desconto de frete do vendedor.
  [OFICIAL] kid=5665577566734097, 2026-08-31. A FAQ da página cita "vendedores no México", sinal de tradução adaptada.
- **O algoritmo favoreceria quem despacha em até 48 horas.** [DADO] Mundo do Marketing, 2026-08-19, sem fonte oficial. Não há confirmação em N1.

### 2.6 Loja nova: limite de pedidos
| Nível | Pedidos/dia | Anúncios ativos | Para chegar (resumo) |
|---|---|---|---|
| Iniciante | 50 | 1.000 | Padrão de entrada |
| Padrão | 100 | 2.000 | ≥ 30 dias, ≥ 10 anúncios, questionário, ≥ 50 pedidos entregues, ≥ 10 compradores únicos, < 4 violações em 30 dias, SPS ≥ 3,0 |
| Premium | 200 | 3.000 | ≥ 100 entregues, ≥ 20 compradores, SPS ≥ 3,5 |
| Profissional | Ilimitado | Ilimitado | Promoção automática; dá para pular nível |

[OFICIAL] kid=1444948507379472, 2026-04-02 (pode estar superada). A tabela veio desalinhada na leitura e precisa ser conferida no navegador. O limite também pode baixar "enquanto o TikTok Shop conclui verificações de segurança".

### 2.7 Cancelamento, devolução e reembolso
- **Janelas do comprador:**
  - devolução e reembolso em 30 dias corridos depois de "Entregue";
  - defeito em até 90 dias;
  - "a lei brasileira" segue valendo depois disso. A página não cita os 7 dias do CDC.
  [OFICIAL] kid=894339073115921, 2026-09-24.
- **Prazos do vendedor:**
  - cancelamento ou reembolso sem resposta em 24 horas é aprovado automaticamente;
  - categorias que exigem aprovação têm 3 dias úteis;
  - depois de receber a devolução, o vendedor tem 2 dias úteis para agir;
  - o comprador tem 14 dias para postar a devolução;
  - disputa em até 15 dias depois da aprovação automática.
  [OFICIAL] kid=894339073115921.
- **Frete de volta:**

  | Motivo | Quem paga |
  |---|---|
  | "Não preciso mais"; tamanho ou caimento (moda) | TikTok Shop |
  | Descrição imprecisa, peça faltando ou quebrada, dano com caixa intacta, defeito, item errado, "chegou tarde" | Vendedor |

  [OFICIAL] kid=894339073115921. No SFP, quando a culpa é do vendedor, ele paga a logística de ida e a de volta sem subsídio. Sem culpa do vendedor, ele não paga a reversa. [OFICIAL] kid=5665577566734097.
- **Reembolso sem devolução:**
  - automático até R$ 25 por item, com o custo do produto coberto pela plataforma (medida temporária);
  - o vendedor pode criar regras próprias por categoria, motivo ou faixa de preço;
  - devolução deixada em ponto designado gera reembolso automático ao comprador, exceto itens de R$ 160 ou mais.
  [OFICIAL] kid=894339073115921.
- **Restrições:**
  - materiais perigosos, consumíveis e personalizados não são retornáveis;
  - **alimentos, bebidas, cosméticos e perfumes devem voltar lacrados**, e o vendedor pode recusar se vierem abertos, salvo defeito.
  [OFICIAL] kid=894339073115921. A mesma página põe "consumíveis" como não retornáveis e "alimentos" como retornáveis se lacrados. Pede leitura no navegador.
- **Dano em trânsito.** A plataforma decide pela embalagem externa. Caixa amassada, molhada ou violada aponta para o transporte, e o vendedor não é penalizado. Caixa intacta com produto quebrado aponta para o vendedor. [PRÁTICA] ub2-x9aJ4QE, 2026-04-28. Reclamação contra a transportadora, se aprovada, compensa o vendedor em até 5 dias úteis. [OFICIAL] kid=894339073115921.
- **Embalagem e etiqueta (proibições):**
  - material promocional não solicitado, brinde não pedido e mensagem que peça avaliação positiva ou ofereça benefício para não devolver;
  - QR code, hiperlink ou contato de outra plataforma na etiqueta.
  [OFICIAL] kid=1442971111884545 (pode estar superada).

### 2.8 Amostras para criadores
- Produto e frete são 100% do vendedor, e o SFP não se aplica. O vendedor tem 7 dias para aprovar a solicitação, senão a plataforma cancela. A amostra entra como pedido comum com a etiqueta "Amostra grátis do vendedor" e sai pelo fluxo normal. [OFICIAL] kid=6589441682917136, 2026-02-05 (pode estar superada); kid=5665577566734097.
- A página não dá prazo de envio da amostra. **Amostras ficam fora do LDR e do SFCR.** [OFICIAL] kid=3321767214286609; kid=3333356285478657.
- O criador tem 14 dias para publicar. [OFICIAL] kid=6589441682917136.

---

## 3. O que os melhores fazem

### 3.1 Consenso
1. **Despachar antes do prazo, não no prazo.**
   - KMZ8gimnMhc (fábrica de camisetas, ~1.000 pedidos/dia, 2026-08-03): a operação leva pacotes ao ponto de postagem **três vezes ao dia**, em vez de esperar a coleta com horário incerto. [CASE]
   - 9l6u6uw-85k: não deixar para a última hora e escolher horário de pouco movimento no ponto. [PRÁTICA]
   - Xs43fCYFsQ8: começar com 2 dias de manuseio e só reduzir para 1 depois de cumprir o indicador. [PRÁTICA] (EUA)
2. **Estoque real e integrado, nunca "fake".** ERP integrado (Bling, Tiny, UpSeller) com NF-e automática para não vender o que acabou.
   - Fontes: [PRÁTICA] 9l6u6uw-85k; 94_XEnheB5Q (Sebrae PR, 2026-08-11); 9w2ndZKzsIQ; W6 em `../social/notas.md`.
   - Motivo citado: no TikTok Shop o afiliado escolhe o produto sem avisar ("vendeu 300 peças e você não tem"). [PRÁTICA] 9l6u6uw-85k.
3. **Provar tudo com data e hora.**
   - Foto do ponto de coleta, vídeo da embalagem de item frágil, vídeo da abertura da devolução. [PRÁTICA] 9l6u6uw-85k; ub2-x9aJ4QE.
   - É o que a lista oficial de recurso pede. [OFICIAL] kid=3026645972993808.
4. **Embalagem como defesa.** Reforço de cantos, itens frágeis embalados um a um, caixa sem espaço vazio e conferência de variante antes de fechar. [OFICIAL] 7678914620211383573 (2026-08-28); 7678673969184230677 (2026-08-27).
   - Quantidade de título, imagem e SKU precisa bater ("kit" com SKU de 1 unidade gera violação). [OFICIAL] 7678673969184230677.
5. **Penalidade logística atinge o afiliado.** A agência diz que penalidade reduz o fluxo de pedidos e derruba a comissão dos afiliados. [PRÁTICA] 7673494161630235925. Na Always Fit, com o OVL de 1.000 pedidos/dia, o limite estourava "11 horas da manhã, meio-dia" e o carrinho dos afiliados parava; os sócios dizem que afiliados migraram para concorrentes. [CASE] z-Nq9_kLbQ8; 6sWUmzRywWU.

### 3.2 Dimensionar estoque para pico viral e LIVE
- **Concentrar o catálogo.** A Always Fit mantém 8 a 10 produtos no TikTok Shop, contra mais de 80 no site. O motivo: se um criador viraliza um item "parado", as fábricas não acompanham e "vai dar punição". [CASE] z-Nq9_kLbQ8, 2025-11-25.
- **Capacidade de produção redundante.**
  - Uma fábrica fazia 95% da produção e não aguentou; a marca abriu fábricas parceiras às pressas. [CASE] z-Nq9_kLbQ8.
  - Em 2026 a marca tem fábrica própria e "mais 48" terceiras. [CASE] 6sWUmzRywWU.
  - Em crise trocou de operador logístico em 3 dias (33 a 36 carretas de estoque) e exigiu rótulo entregue no mesmo dia. [CASE] 6sWUmzRywWU.
  - Antes, rótulo levava 20 dias e produto mais 10. [CASE] 6sWUmzRywWU (episódio de 2023, anterior ao TikTok Shop BR e em outro canal; serve como mecânica de prazo de reposição).
- **Operador terceirizado com WMS integrado.** O pedido cai no WMS do operador, que separa e envia, e o vendedor só precisa do ERP para a NF-e. [CASE] z-Nq9_kLbQ8.
- **Kits para ganhar volume sem multiplicar pacotes.** 1.000 pedidos/dia equivalem a ~3.000 peças. [CASE] KMZ8gimnMhc.
- **Produção sob demanda sobre estoque único.** A camiseta lisa fica em estoque e a estampa é aplicada conforme o pedido. [CASE] KMZ8gimnMhc.
- **Estoque de segurança por canal (EUA):** com estoque compartilhado no Amazon MCF, reservar 50 a 100 unidades para a listagem do TikTok "esgotar" antes de zerar a Amazon. [PRÁTICA] 6hi05eKvkyM (Helium 10, 2025-12-19; vende software).
- **Folga de 30 dias nos campeões.** [PRÁTICA] L5CnT13a8PI (EUA, 2026-06-24; agência).
- **Antecipar datas.** Planejar Natal e Black Friday e tirar a loja do período de loja nova meses antes, para não chegar à data com teto de pedidos. [PRÁTICA] 9l6u6uw-85k (vende treinamento).
- **Negociar frete.** Leilão entre transportadoras, negociando já para o volume projetado. [PRÁTICA] 6sWUmzRywWU. No Enviado pela Plataforma isso só vale para amostra ou Envio pelo Vendedor.

### 3.3 Evidência de ruptura depois de viral ou campanha
| Caso | Fato narrado | País | Tipo |
|---|---|---|---|
| Always Fit, 10/10 de 2025 | De ~1.000 para mais de 10.000 pedidos/dia; atraso; punição com teto de 1.000/dia; perda estimada de R$ 1 a 1,5 mi | BR | [CASE] z-Nq9_kLbQ8 |
| Always Fit, início no TikTok Shop | O operador logístico "não estava aguentando"; cancelamento automático por atraso; afiliados foram para concorrentes | BR | [CASE] 6sWUmzRywWU |
| Marca de consumo (Helium 10) | Viral: 3.000 unidades em 2 dias; ruptura de 3 meses, inclusive na Amazon | EUA | [CASE] 6hi05eKvkyM |
| Cliente da Profitable Pineapple | "Forçamos o cliente a ficar sem estoque" a ~US$ 1 mi de run rate | EUA | [CASE] -TXa-4jZc1s (pitch comercial, sem dado verificável) |
| Medicube (Kalodata) | 3,6% dos compradores reclamam; ~60% das reclamações são de envio e embalagem (vazamento, tampa quebrada) | EUA | [DADO] estimativa de ferramenta citada em PkW3bkdFbCM, 2026-10-02 |

Nenhum dado agregado (frequência de ruptura por produto viral) foi encontrado para o BR.

### 3.4 Amostras na prática
- **A amostra disputa o mesmo estoque do pico.** Com estoque raso, não compensa espalhar amostras. [PRÁTICA] 7684307680252497173 (vende curso).
- **Em escala, a amostra vira uma operação logística própria.** A Always Fit chegou a 15 a 20 mil amostras por mês e depois criou uma área só para filtrar quem recebe, porque "queima muita grana". [CASE] 6sWUmzRywWU.
- **Nos EUA, o FBT envia amostras pelo mesmo fluxo dos pedidos, em ~3 dias.** Sem fulfillment, a agência estima ~1 semana até o criador receber. [PRÁTICA] L5CnT13a8PI (EUA; agência).
- **Fiscal (BR):** cadastrar no produto a natureza de operação de bonificação, senão a nota da amostra não sai. [PRÁTICA] 9w2ndZKzsIQ.

### 3.5 Divergências
1. **Onde o atraso pesa mais:** prazo de despacho (oficial) × prazo de entrega.
   - Um afiliado diz que a transportadora própria vai acabar com o atraso e que entrega rápida aumenta a recompra ("mais de 70%" dos brasileiros, sem fonte). [PRÁTICA] 4LnQ0HB6A_Q (conflito de interesse: vende ferramenta e curso).
   - A política mede o vendedor só até o TTS. Atraso da transportadora no Envio pelo TikTok vai para chamado e recurso. [OFICIAL] kid=1442971111884545.
2. **FBT vale a pena? (EUA)**
   - A favor: "9 em 10 vezes" recomenda FBT. [PRÁTICA] Xs43fCYFsQ8. O FBT também protege o SPS de falhas logísticas e daria +30% de views e +15% a 20% de conversão. [PRÁTICA] L5CnT13a8PI, que cita "dado interno do TikTok" sem fonte primária.
   - Contra: um vendedor testou e voltou ao 3PL, com custo e prazo iguais e o selo sem efeito comprovado. [PRÁTICA] 6hi05eKvkyM.
   - **Irrelevante para o BR hoje (não há FBT)**, mas mostra o que pode chegar.
3. **Cancelamento automático em 6 dias úteis (oficial) × "hoje é três" (Always Fit).** Ver §2.2.
4. **Cartão pedindo avaliação dentro do pacote.**
   - Prática recomendada nos EUA. [PRÁTICA] PkW3bkdFbCM (EUA).
   - A Política de Envio BR proíbe mensagem pedindo avaliação positiva. [OFICIAL] kid=1442971111884545.

---

## 4. Números de referência
| Número | Valor | Fonte | Data | País | Tipo |
|---|---|---|---|---|---|
| SLA de pronto para envio | 1 dia útil | kid=1444948508280592 | 2026-09-30 | BR | [OFICIAL] |
| SLA de TTS/despacho | 2 dias úteis, corte 23:59:59 UTC-3 | kid=1444948508280592; kid=3321767214286609 | 2026-09-30 | BR | [OFICIAL] |
| Cancelamento automático | 6 dias úteis | idem; kid=894339073115921 | 2026-09 | BR | [OFICIAL] |
| SLA anterior | 3 dias úteis; cancelamento em 7 | 7510044886742125829 | 2025-05-30 | BR | [OFICIAL] (pode estar superada) |
| LDR máximo | 4% | kid=3321767214286609 | 2026-08-26 | BR | [OFICIAL] |
| SFCR máximo | 2,5% (janela de 7 dias) | kid=3333356285478657 | 2026-07-14 | BR | [OFICIAL] |
| FDR recomendado | ≥ 90% em 1 dia útil | kid=1444948508280592 | 2026-09-30 | BR | [OFICIAL] |
| VTR mínimo | 95% | kid=1444948508280592 | 2026-09-30 | BR | [OFICIAL] |
| Pick-up pela transportadora | até 48 h depois de "Organizar envio" | kid=1442971111884545 | 2026-03-06 | BR | [OFICIAL] (pode estar superada) |
| Correção de rastreio | 72 h | kid=1442971111884545 | 2026-03-06 | BR | [OFICIAL] (pode estar superada) |
| SPS exibido | ≥ 30 pedidos em 60 dias | kid=7517966208927489 | 2026-07-07 | BR | [OFICIAL] |
| SPS para campanha | ≥ 3,0 | kid=2996214162966289 | 2026-07-24 | BR | [OFICIAL] |
| Pedidos/dia da loja nova | 50 / 100 / 200 / ilimitado | kid=1444948507379472 | 2026-04-02 | BR | [OFICIAL] (pode estar superada) |
| SFP (frete grátis) | 6% do preço, teto de R$ 50 por produto | kid=5665577566734097 | 2026-08-31 | BR | [OFICIAL] |
| Subsídio de frete ao comprador | De R$ 5 (novo, compra ≥ R$ 109) a R$ 40 (nível 3, compra ≥ R$ 159) | kid=5665577566734097 | 2026-08-31 | BR | [OFICIAL] |
| Reembolso sem devolução | Automático até R$ 25 | kid=894339073115921 | 2026-09-24 | BR | [OFICIAL] |
| Janela de devolução | 30 dias (defeito: 90) | kid=894339073115921 | 2026-09-24 | BR | [OFICIAL] |
| Limites de pacote | 30 kg; 100 cm; 200 cm | ANYMARKET | 2026-09-15 | BR | [DADO] terceiro |
| Capital da TikTok Logistics Brazil | R$ 111 mi | Fast Company Brasil | 2026-08-19 | BR | [DADO] |
| E-commerce BR (todos os canais), Semana do Consumidor | 6% dos pedidos com frete grátis (22% no Norte, 4% no Sudeste); prazo médio de 3 dias (~48 h no Sudeste, até 11 dias no Norte); frete médio de R$ 34 | Frete Rápido (nstech), >500 mil pedidos de >250 lojas, 9 a 16/03/2026, via Mundo do Marketing | 2026-04-16 | BR | [DADO] com amostra declarada; não é TikTok Shop |
| Compra concluída depois de descobrir no TikTok | 57,8% | Pesquisa in-app com 17 mil usuários, Newsroom TikTok | 2026-06-04 | BR | [DADO] da própria plataforma, sem instituto ou margem |
| Pico de um top seller | ~1.000 para >10.000 pedidos/dia no 10/10 | z-Nq9_kLbQ8 | 2025-11-25 | BR | [CASE] |
| Volume de um top seller | ~20.000 pedidos/dia; ~10 reclamações/dia no Reclame Aqui | 6sWUmzRywWU | 2026-10-13 | BR | [CASE] |
| Devolução numa fábrica de moda | "Nunca passou de 2%" | KMZ8gimnMhc | 2026-08-03 | BR | [CASE] |
| OVL por faixa de LDR | 10% a 30%: 90% do volume médio; 30% a 50%: 70%; >50%: 50% | BigSeller | 2024-09 | Malásia | [DADO] (pode estar superada) |
| Custo por unidade (EUA) | Seller ~US$ 8; TikTok Shipping ~US$ 5,68; FBT ~US$ 4,70 | Tela do Seller Center mostrada em Xs43fCYFsQ8 | 2025-12-19 | EUA | [PRÁTICA] (pode estar superada) |
| Tarifa FBT (EUA) | US$ 3,58/un. (1 item) e US$ 2,86/un. (multi-item); armazenagem grátis por 30 ou 60 dias (fontes divergem) | amzprep; dashboardly; shortformnation | 2026 | EUA | [DADO] terceiros em conflito |
| Efeito do selo de 3 dias (EUA) | +30% views; +15% a 20% conversão | L5CnT13a8PI ("dado interno do TikTok") | 2026-06-24 | EUA | [PRÁTICA] sem fonte primária |

Cobertura de dados com método: três fontes têm amostra declarada (Frete Rápido; pesquisa in-app do TikTok; estimativa da Kalodata para a Medicube, EUA). Nenhuma mede desempenho logístico **do TikTok Shop BR** (LDR médio, prazo médio, taxa de ruptura).

---

## 5. Alimentos, café e marca própria/indústria

1. **O que pode e o que não pode.**
   - Proibidos sem exceção: perecível, item que exige temperatura controlada, alimento caseiro, aditivo e vencido. [OFICIAL] kid=6483182812481296, 2026-08-17.
   - Embalado ou pré-embalado e bebida não alcoólica só com qualificação (categoria só para convidados). [OFICIAL] kid=6483182812481296; kid=6504327061473040 (2026-04-30).
   - Café não é citado nominalmente. Café torrado embalado cai, por inferência, em "alimento pré-embalado". [OBS] inferência desta frente.
2. **Validade e giro.**
   - A política proíbe vendido vencido e não define validade mínima no envio (lacuna, §9).
   - Fabricante de suplemento diz que o produto "chega hoje e sai amanhã", sem estoque parado. [CASE] z-Nq9_kLbQ8.
   - Num produto com validade, a mecânica do pico obriga a escolher entre ruptura (penalidade) e excesso (vencimento). A lição prática que aparece é manter poucos SKUs com fábrica de resposta rápida.
3. **Embalagem.**
   - Não há regra oficial específica de alimento além da genérica (proteção, sem espaço vazio).
   - Na devolução, alimento só volta se lacrado. [OFICIAL] kid=894339073115921. Lacre de segurança vira prova para recusar devolução aberta.
   - O caso Medicube (EUA) mostra o risco das embalagens líquidas: vazamento e tampa quebrada dominaram as reclamações. [DADO] PkW3bkdFbCM.
4. **Frete e ticket.**
   - O SFP cobra 6% sobre o preço com teto de R$ 50. No ticket de alimento, o teto não chega a atuar.
   - O subsídio ao comprador tem degraus de compra mínima (R$ 9, 29, 39, 69, 109, 139, 159), o que dá à plataforma uma alavanca natural para kits. [OFICIAL] kid=5665577566734097.
   - Pacote de 1 kg é o formato mais citado nas legendas de café observadas. [OBS] `../observacao/vitrine.md`.
   - Peso entra no frete, mas o limite de 30 kg não preocupa no café.
5. **Reembolso sem devolução até R$ 25** (temporário e coberto pela plataforma) favorece o comprador no ticket baixo. Isso pesa em produto alimentar barato. [OFICIAL] kid=894339073115921.
6. **Indústria × pico.** O gargalo citado pelos fabricantes não é o transporte, mas rótulo, insumo e capacidade de fábrica (20 dias de rótulo + 10 de produção num episódio). Os grandes respondem com fornecedor de rótulo no mesmo dia e várias fábricas terceiras. [CASE] 6sWUmzRywWU; z-Nq9_kLbQ8.
7. **Nenhuma fonte social ensina logística de alimento no TikTok Shop BR.** [OBS] `../social/notas.md` §7.

---

## 6. Erros comuns e mitos
| Mito ou erro | O que as fontes mostram |
|---|---|
| "O TikTok vai cobrar taxa por atraso" | Não há taxa: o atraso gera advertência, OVL, restrição de campanha e dedução de saldo (por SFCR). [OFICIAL] kid=3321767214286609; [PRÁTICA] 9l6u6uw-85k |
| "O seller shipping acabou" | Mensagem dos EUA (fev/2026), cujo prazo foi suspenso. [OFICIAL via terceiro] ChannelX, 2026-02-18. No BR o Envio pelo Vendedor está previsto e se expande. q2QT6vmni2s e L5CnT13a8PI repetem a versão superada |
| "Tem FBT/fulfillment no Brasil" | Não há. Vídeos em português dublados dos EUA (5wMocFaES44, U7Vz5xqNeNc) falam em FBT/TFS e centro de distribuição "nos EUA". País trocado |
| "Com a transportadora própria nunca mais vai ter atraso" e "frete grátis para todos" | A empresa existe, mas não há data de operação nem fim das parcerias. O próprio vídeo desmente o frete grátis universal. [PRÁTICA] 4LnQ0HB6A_Q; [DADO] ANYMARKET |
| "Viral justifica atraso no recurso" | Pico, campanha e falta de estoque não estão na lista fechada de recursos. [OFICIAL] kid=3026645972993808 |
| "Produto esgotado = sem estoque" | Pode ser OVL: com limite atingido, o produto aparece "Esgotado". [OFICIAL] kid=3309653722089232 |
| Lançar com criador grande na semana 1 | Com teto de 50 pedidos/dia, o produto "esgota" logo no início do dia. [OFICIAL] kid=1444948507379472; [CASE] z-Nq9_kLbQ8 |
| Mandar cartão pedindo 5 estrelas ou brinde extra no pacote | Proibido pela Política de Envio BR. [OFICIAL] kid=1442971111884545 |
| Comprar de outro marketplace e mandar direto ao cliente | Dropshipping e logística internacional são proibidos para vendedor BR. [OFICIAL] kid=1442971111884545 |
| Achar que o 6% do frete volta na devolução | Não volta em pedido enviado. [OFICIAL] kid=5665577566734097 |
| Esquecer o CFOP de bonificação | A nota da amostra não sai e a amostra trava. [PRÁTICA] 9w2ndZKzsIQ |
| Tratar "FBT dá +30% de views" como fato | Número de agência atribuído a "dado interno", sem fonte primária, dos EUA. Sinal fraco: número de uma fonte só tratado como regra |

Sinais de conteúdo fraco nesta frente:
- **conflito de interesse:** 4LnQ0HB6A_Q, 9l6u6uw-85k e -TXa-4jZc1s vendem curso, treinamento ou ferramenta; xLezRfuG5Tw vende um "vault" de US$ 5;
- **patrocínio no fim:** U7Vz5xqNeNc e ouEgrQvgWF4 terminam com link de crédito de Ads de afiliado;
- **país trocado:** 5wMocFaES44 e U7Vz5xqNeNc;
- **vídeo fora do tema:** vugt-iIrCqI é sobre "entrega do algoritmo", não sobre logística.

---

## 7. Revenda/importação × indústria/marca própria

**[REVENDA] e importação**
- Vendedor BR não pode usar fornecedor ou logística internacional, nem atender pedido com produto comprado de outro varejista ou marketplace. O pedido sai do armazém cadastrado. [OFICIAL] kid=1442971111884545 (pode estar superada). O importador precisa nacionalizar e guardar estoque no Brasil antes de vender.
- O revendedor via afiliado não tem logística (quem entrega é o vendedor). Ele sofre a ruptura e a penalidade do vendedor: perde comissão quando a loja trava. [CASE] 6sWUmzRywWU; [PRÁTICA] 7673494161630235925, 4LnQ0HB6A_Q.
- O revendedor que é vendedor escolhe produto por ferramenta (Kalodata etc.) e corre o risco de comprar estoque do produto errado. [PRÁTICA] q17Fs6PCp8I (EUA; vende ferramenta).

**[MARCA] e indústria**
- O gargalo é produção, rótulo e insumo. A resposta dos grandes: catálogo curto no TikTok, várias fábricas, operador com WMS e negociação de frete. [CASE] z-Nq9_kLbQ8; 6sWUmzRywWU.
- O fabricante usa kits e produção sob demanda para casar volume com capacidade. [CASE] KMZ8gimnMhc.
- O estoque da marca fica exposto a três canais ao mesmo tempo (TikTok, marketplace, site). Em estoque compartilhado, a prática é reservar estoque de segurança por canal. [PRÁTICA] 6hi05eKvkyM (EUA).
- A amostra em grande volume é custo de aquisição e de logística da marca, porque produto e frete são 100% do vendedor. [OFICIAL] kid=6589441682917136; [CASE] 6sWUmzRywWU.

---

## 8. Tabela de afirmações
| id | Afirmação | Tipo | Fonte | Data | País | Confiança |
|---|---|---|---|---|---|---|
| A1 | Envio pelo TikTok e Envio pelo Vendedor: RTS em 1 dia útil e TTS em 2 dias úteis | [OFICIAL] | kid=1444948508280592 | 2026-09-30 | BR | B (tabela truncada na leitura) |
| A2 | Cancelamento automático depois de 6 dias úteis sem "Enviado" | [OFICIAL] | kid=1444948508280592; kid=3321767214286609; kid=894339073115921 | 2026-08/09 | BR | A |
| A3 | LDR ≤ 4%; inclui atrasados não enviados desde 2026-03-16 | [OFICIAL] | kid=3321767214286609; kid=4263127323510529 | 2026-08-26 | BR | A |
| A4 | SFCR ≤ 2,5%, janela de 7 dias, inclui cancelamento automático; amostras excluídas | [OFICIAL] | kid=3333356285478657 | 2026-07-14 | BR | A |
| A5 | FDR recomendado ≥ 90% e VTR ≥ 95% | [OFICIAL] | kid=1444948508280592 | 2026-09-30 | BR | B |
| A6 | Penalidades: OVL, restrição de campanha e dedução de saldo; não há taxa por atraso | [OFICIAL] | kid=3333356285478657; kid=1444948508280592 | 2026-07/09 | BR | A |
| A7 | Com OVL ativo, o produto aparece "Esgotado" | [OFICIAL] | kid=3309653722089232 | 2025-10-27 | BR | B (pode estar superada) |
| A8 | Recurso de LDR: só falha de coleta, ponto fechado, feriado municipal, sistema, força maior e pedido do cliente | [OFICIAL] | kid=3026645972993808 | 2026-03-06 | BR | B (pode estar superada) |
| A9 | Loja nova: 50/100/200/ilimitado pedidos por dia | [OFICIAL] | kid=1444948507379472 | 2026-04-02 | BR | B (pode estar superada) |
| A10 | SPS exibido só com 30 pedidos em 60 dias; campanha exige SPS ≥ 3,0 | [OFICIAL] | kid=7517966208927489; kid=2996214162966289 | 2026-07 | BR | A |
| A11 | Dois SFCR seguidos em campanha geram período de cancelamento obrigatório | [OFICIAL] | kid=2996214162966289 | 2026-07-24 | BR | A |
| A12 | SFP: 6% do preço, teto de R$ 50; não volta em devolução de pedido enviado | [OFICIAL] | kid=5665577566734097 | 2026-08-31 | BR | A |
| A13 | Produto com "má experiência" sai da lista de frete grátis; atraso excessivo pode suspender a participação | [OFICIAL] | kid=5665577566734097 | 2026-08-31 | BR | B (critério não definido) |
| A14 | Amostra: produto e frete 100% do vendedor; SFP não se aplica; aprovação em 7 dias | [OFICIAL] | kid=6589441682917136; kid=5665577566734097 | 2026-02/08 | BR | A |
| A15 | Frete de volta: TikTok paga "não preciso mais" e tamanho (moda); vendedor paga defeito, erro, falta, atraso | [OFICIAL] | kid=894339073115921 | 2026-09-24 | BR | A |
| A16 | Reembolso sem devolução automático até R$ 25, coberto pela plataforma (temporário) | [OFICIAL] | kid=894339073115921 | 2026-09-24 | BR | B |
| A17 | Alimento e bebida devolvidos devem vir lacrados | [OFICIAL] | kid=894339073115921 | 2026-09-24 | BR | B (página contraditória sobre consumíveis) |
| A18 | Perecível, temperatura controlada, caseiro, aditivo e vencido são proibidos | [OFICIAL] | kid=6483182812481296 | 2026-08-17 | BR | A |
| A19 | Vendedor BR não pode usar dropshipping nem logística internacional | [OFICIAL] | kid=1442971111884545 | 2026-03-06 | BR | B (pode estar superada) |
| A20 | Pick-up em até 48 h; correção de rastreio em 72 h | [OFICIAL] | kid=1442971111884545 | 2026-03-06 | BR | B (pode estar superada) |
| A21 | Proibido material promocional ou mensagem pedindo avaliação no pacote | [OFICIAL] | kid=1442971111884545 | 2026-03-06 | BR | B (pode estar superada) |
| A22 | Não há fulfillment da plataforma no BR | [DADO] | ANYMARKET; UpSeller | 2026-08/09 | BR | B |
| A23 | Transportadoras: J&T, Correios, iMile; Total Express e Jadlog como postagem; reversa nos Correios | [DADO] | Central do Varejo; UpSeller | 2026-08 | BR | B |
| A24 | Limites de pacote: 30 kg, 100 cm, 200 cm | [DADO] | ANYMARKET | 2026-09-15 | BR | C |
| A25 | TikTok Logistics Brazil com capital de R$ 111 mi, sem data de operação | [DADO] | Fast Company Brasil; ANYMARKET | 2026-08/09 | BR | A (existência) / C (operação) |
| A26 | Frete ajustado em rotas que saem de SP, RJ, MG e ES no Enviado pela Plataforma | [DADO] | Mundo do Marketing | 2026-08-19 | BR | C |
| A27 | Algoritmo favorece quem despacha em 48 h | [DADO] | Mundo do Marketing | 2026-08-19 | BR | C |
| A28 | Always Fit: pico de ~1.000 para >10.000 pedidos/dia; OVL de 1.000/dia; perda de R$ 1 a 1,5 mi | [CASE] | z-Nq9_kLbQ8 | 2025-11-25 | BR | C |
| A29 | Always Fit mantém 8 a 10 SKUs no TikTok contra 80 no site para controlar pico | [CASE] | z-Nq9_kLbQ8 | 2025-11-25 | BR | C |
| A30 | Fábrica com 1.000 pedidos/dia posta 3 vezes ao dia no ponto, em vez de esperar coleta | [CASE] | KMZ8gimnMhc | 2026-08-03 | BR | C |
| A31 | Viral: 3.000 unidades em 2 dias e 3 meses de ruptura | [CASE] | 6hi05eKvkyM | 2025-12-19 | EUA | C |
| A32 | OVL por faixa de LDR: 90%/70%/50% do volume médio | [DADO] | BigSeller | 2024-09 | Malásia | B (pode estar superada; não vale para BR) |
| A33 | US suspendeu o fim do Seller Shipping previsto para 25/02/2026 | [OFICIAL via terceiro] | ChannelX | 2026-02-18 | EUA | B |
| A34 | Selo FBT de 3 dias: +30% views e +15% a 20% conversão | [PRÁTICA] | L5CnT13a8PI | 2026-06-24 | EUA | C |
| A35 | E-commerce BR: 6% dos pedidos com frete grátis; prazo médio de 3 dias | [DADO] | Frete Rápido via Mundo do Marketing | 2026-04-16 | BR | B (amostra declarada; não é TikTok Shop) |
| A36 | Cancelamento por atraso "hoje é três" dias | [CASE] | 6sWUmzRywWU | 2026-10-13 | BR | C (contradiz A2) |

---

## 9. Lacunas
1. **Guia do Usuário sobre Envio pelo Vendedor (BR)** não foi encontrado: quais LSPs são "compatíveis", critério de aprovação e TMS exigido.
2. **Lista oficial de transportadoras e regiões de coleta** só veio pela imprensa. A página da plataforma citada pela Central do Varejo não foi localizada.
3. **O que é "significativamente acima de 4%"** e como o OVL é calculado no BR (percentual do volume médio? por quantos dias?) não aparece em N1. Só há a referência da Malásia.
4. **Janela do LDR** ("período aplicável") e janelas de FDR e VTR não foram ditas.
5. **SPS BR:** pesos e lista completa de métricas não foram encontrados (a página de diagnóstico `seller-br.tiktok.com/health-center/experience-score?shop_region=BR` exige login).
6. **Critério de "má experiência"** para tirar o produto do frete grátis não está definido.
7. **Prazo de envio da amostra** e consequência do não envio não estão na página de amostras de fev/2026.
8. **Divergência 6 dias úteis × "três dias"** de cancelamento: confirmar no navegador.
9. **Data de operação e escopo da TikTok Logistics Brazil**, CDs e planos de fulfillment: só há especulação de imprensa.
10. **Validade mínima no envio, temperatura no transporte e embalagem de alimento:** não há regra oficial específica. Falta ler na íntegra a Política de Produtos Restritos de alimentos e a página da categoria.
11. **Não há dado agregado do TikTok Shop BR** sobre LDR médio, prazo médio de entrega, taxa de devolução por categoria ou frequência de ruptura depois de viral. Nenhuma ferramenta N5 publica isso.
12. **Corte do ponto de postagem** ("o TikTok corta 4 horas", KMZ8gimnMhc) não foi explicado: pode ser horário de corte do ponto ou da plataforma.
13. **Páginas para conferir no navegador** (tabelas truncadas ou contraditórias na leitura):
    - kid=1444948508280592 (tabela de SLA);
    - kid=1444948507379472 (tabela de níveis);
    - kid=894339073115921 (consumíveis × alimentos lacrados; 2 × 3 dias para "somente reembolso");
    - kid=2583991870097169 e kid=2578485181925121 (guias de cancelamento e devolução, não lidos);
    - kid=6843306600302353 (item faltando ou errado, não lido).

Uso de ferramentas desta frente: 6 WebSearch e 22 WebFetch. Foram lidas 13 transcrições designadas e 9 de outros temas com trechos de logística: ub2-x9aJ4QE, 9l6u6uw-85k, KMZ8gimnMhc, z-Nq9_kLbQ8, 6sWUmzRywWU, 94_XEnheB5Q, PkW3bkdFbCM, YOSCEWDEstE e p7BZwvm2Y_c.

## 10. Verificação web (2026-10-15)

Método: WebFetch direto em cada página da Seller University BR (seller-br.tiktok.com/university/essay?knowledge_id=<kid>), sem login e sem WebSearch. A data de cada página é a que ela mostra. Páginas com mais de 6 meses levam "pode estar superada". Todas são [OFICIAL], Brasil.

| id | veredito | fonte oficial | observação |
|---|---|---|---|
| A1 | PENDENTE NAVEGADOR | kid=1444948508280592 (2026-09-30); kid=3321767214286609 (2026-08-26) | TTS em 2 dias úteis com corte 23:59:59 (UTC-3): confirmado em duas páginas, e a de LDR diz que o SLA de 2 dias vale para envio via TikTok ou vendedor. O "pronto para envio em 1 dia útil" só aparece como inferência, porque as células da tabela de SLA vêm vazias na leitura. Conferir a tabela renderizada. |
| A2 | CONFIRMADA | kid=1444948508280592 (2026-09-30); kid=3321767214286609 (2026-08-26); kid=894339073115921 (2026-09-24) | Seis dias úteis nas três páginas. A kid=894339073115921 liga o cancelamento ao pedido que não chega a "TTS" (em trânsito para envio), e as outras duas falam em "Enviado". Nenhuma página oficial traz "três dias": o "hoje é três" do caso Always Fit não tem respaldo nelas. |
| A3 | CONFIRMADA | kid=3321767214286609 (2026-08-26); kid=4263127323510529 (anúncio de 2026-03-10, vigência 2026-03-16) | Meta ≤ 4% "o tempo todo". Inclui enviados com atraso e pedidos ainda sem envio após o prazo. Amostra grátis e pedido cancelado antes do SLA ficam fora. |
| A4 | CONFIRMADA | kid=3333356285478657 (2026-07-14) | ≤ 2,5% sobre pedidos em 7 dias corridos. Inclui cancelamento automático por erro do vendedor na preparação ou entrega. A exclusão de amostras para o SFCR não apareceu na leitura desta verificação (a nota já a atribui à mesma página). |
| A5 | CONFIRMADA | kid=1444948508280592 (2026-09-30) | FDR ≥ 90% (envio em até 1 dia útil), que a página trata como meta a perseguir. VTR ≥ 95%. |
| A7 | CONFIRMADA | kid=3309653722089232 (2025-10-27, pode estar superada) | Com o limite atingido, os produtos aparecem como "Esgotado" e a loja deixa de receber pedidos. O OVL é redefinido no início de cada dia do calendário. |
| A8 | CONFIRMADA | kid=3026645972993808 (2026-03-06, pode estar superada) | Lista fechada: falha de coleta, ponto de postagem fechado ou lento, erro de sistema, força maior, pedido do comprador e feriado municipal fora do calendário. Qualquer cenário fora da lista não é aceito, o que exclui pico viral por omissão (a página não cita "viral"). |
| A9 | CONFIRMADA | kid=1444948507379472 (2026-04-02, pode estar superada) | 50 (Iniciante), 100 (Padrão), 200 (Premium) e sem limite (Profissional). A página avisa que os limites podem ser afetados durante verificações de segurança. A tabela foi lida sem desalinhamento, mas só os pedidos/dia foram conferidos aqui. |
| A11 | CONFIRMADA | kid=2996214162966289 (2026-07-24) | SPS ≥ 3,0 desde abril de 2026. Duas violações consecutivas de SFCR em campanhas levam a período de cancelamento obrigatório na campanha seguinte. A regra sobre loja sem SPS (sem penalidade de LDR/SFCR) vale desde agosto de 2026. |
| A13 | CONFIRMADA | kid=5665577566734097 (2026-08-31) | Produto com experiência ruim pode sair da lista de frete grátis e o comprador passa a pagar o frete. O TikTok pode suspender ou encerrar a participação por "atrasos excessivos de entrega", avaliações negativas constantes e falhas de embalagem e etiqueta. "Má experiência" segue sem definição na página. Confirmado também 6% sobre o preço de venda de produtos entregues, com teto de R$ 50 por produto. |
| A16 | CONFIRMADA | kid=894339073115921 (2026-09-24) | Reembolso sem devolução automático para preço de compra de até R$ 25,00 (sem frete, impostos e taxas). A plataforma cobre o custo total do produto nesse reembolso obrigatório, descrito como "medida temporária até novo aviso", sem data de fim. Alimentos e bebidas devem voltar lacrados e fechados, e o vendedor pode recusar item aberto, salvo defeito ou responsabilidade do vendedor. |
| A19 | CONFIRMADA | kid=1442971111884545 (2026-03-06, pode estar superada) | Vendedor baseado no Brasil não pode usar fornecedor terceirizado internacional nem logística internacional. Só logística doméstica, a partir do armazém cadastrado. Comprar de outro varejista para enviar direto ao cliente é tratado como fraude. Pick-up pela transportadora em até 48 h depois de "Organizar envio". Correção de rastreio em 72 h. |

Resumo: 11 confirmadas, 0 contestadas, 0 sem fonte oficial, 1 pendente de navegador (A1). Nenhuma busca web foi usada.


## 11. Verificação pelo navegador (2026-10-15)

Método: Claude in Chrome, leitura renderizada (JavaScript) da Academy BR (seller-br.tiktok.com/university), da busca interna da Academy, do Newsroom pt-BR e de vídeo oficial. Sem login, sem captcha. Paráfrase; citação literal no TSV (verificacao/resultado.tsv).

| id | veredito | fonte | observação |
|---|---|---|---|
| A1 | CONFIRMADA | seller-br.tiktok.com kid=1444948508280592 (2026-09-30, BR) [OFICIAL] | Tabela renderizada: "Pronto para envio" (RTS) recomendado em 1 dia útil a partir do pedido e TTS em 2 dias úteis, para Envio pelo TikTok e Envio pelo Vendedor; cancelamento automático se não "Enviado" em 6 dias úteis. O RTS é prazo recomendado, não limite. |
