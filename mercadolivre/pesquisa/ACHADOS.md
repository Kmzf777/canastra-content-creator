# O que os vídeos recentes corrigiram na estratégia

> **Janela:** vídeos publicados entre 04/08/2026 e 25/09/2026 (últimos 60 dias).
> **Método:** 16 transcrições baixadas com `yt-dlp` e varridas por tema com
> `varrer.py`. Todo item abaixo cita canal, data e ID do vídeo.
>
> **Por que isto existe:** boa parte de `docs/ML-CAPSULAS-ESTRATEGIA.md` estava
> apoiada em blog de agência, não em fonte primária nem em prática recente. Esta
> varredura foi feita para derrubar ou confirmar essas afirmações.

---

## Reproduzir a pesquisa

```bash
cd docs/pesquisa-ml
python pesquisar.py 60        # busca + filtra por data -> videos.tsv
python baixar.py              # baixa legendas -> transcricoes/*.txt (pula o que já existe)
python varrer.py              # lista temas
python varrer.py premium      # trechos sobre clássico vs premium
```

Temas disponíveis: `titulo premium roas acos aprendiz frete79 tarifa full
variacao catalogo ficha palavra`.

---

## 1. Brand Ads foi extinto — a fase 2 do playbook não existe mais

> *"Ele vem mudando, já **extinguiu pelo menos temporariamente o Brands** e agora
> ele tá modificando ROAS."*
> — Seus Produtos Na Internet, 25/09/2026 (`ZCSkvBUUddI`)

**O que estava escrito:** "Brand Ads — posição 0, até 200 keywords. Avaliar na
fase 2, depois de reputação verde + Minha Página."

**Correção:** não é avaliável. O formato foi descontinuado, ao menos por ora.
Remover do plano de 90 dias e do playbook.

## 2. Existe ROAS dinâmico — o ROAS fixo virou a opção inferior

> *"Além do ROAS fixo, aquele ROAS que você coloca um número e espera o Mercado
> Livre fazer a mágica, ele agora tá colocando o **ROAS dinâmico**. Ele coloca uma
> **banda** — por exemplo, foi de **4,8 a 7,2**. Se você coloca um ROAS fixo,
> estático, quando a sua concorrência estiver num momento de agressividade (…)
> você vai perder mais leilões, vai ganhar menos, vai ter menos exposição."*
> — Seus Produtos Na Internet, 25/09/2026 (`ZCSkvBUUddI`)

**O que estava escrito:** "ROAS objetivo 7,3× no kit de 40."

**Correção:** o número continua válido como **centro**, mas deve ser configurado
como **banda** se a conta já tiver a função. Um ROAS fixo perde leilão quando o
concorrente fica agressivo. Sugestão: banda em torno de 7,3× — algo como 6,0–8,5×.

**Ressalva:** a função é recentíssima (vídeo de 25/09) e pode não estar liberada
em toda conta. Conferir no gerenciador antes de planejar em cima dela.

## 3. Dá para oferecer Clássico E Premium no mesmo anúncio

> *"E também tem a opção de você **oferecer clássico e premium no mesmo anúncio**.
> Já faz alguns meses que o Mercado Livre disponibilizou essa função."*
> — Ivan Saldanha, 25/08/2026 (`BSNDMsezcbc`)

**O que estava escrito:** "Clássico em tudo; testar Premium só no kit de 100." —
tratado como escolha exclusiva.

**Correção:** não é ou/ou. Se a função estiver disponível na conta, ativar os dois
no mesmo anúncio resolve o dilema inteiro: o comprador que quer parcelar paga a
comissão maior, o que não quer, não paga.

## 4. Regra prática de mercado: abaixo de R$ 400, Clássico

> *"Se for um produto **abaixo de R$ 400**, eu sugiro vocês anunciar no clássico.
> (…) anúncios com ticket mais baixo, eu costumo anunciar **somente no clássico**."*
> — Ivan Saldanha, 25/08/2026 (`BSNDMsezcbc`)

**Efeito:** os três SKUs de cápsula (R$ 32,90 · R$ 129,90 · R$ 179,90) ficam todos
abaixo do corte. Reforça a recomendação de Clássico — agora com apoio de prática,
não só da conta de margem.

## 5. A diferença Clássico→Premium é de 5 pontos — confirmado

> *"O premium é uma comissão **5% acima** do clássico, porque ele parcela em até 12
> vezes para o consumidor final."*
> — IC7 ACADEMY BI, 27/08/2026 (`0InXzo24tWg`)

> *"Comparação entre 11,5, 12% (…) para um anúncio clássico, para mais ou menos
> **16,5, 17** de taxa para um anúncio premium."*
> — Milton P Rabello, 27/08/2026 (`swCx36qRg0w`)

**Confirma** o que estava escrito. Os percentuais citados são de outra categoria
(11,5→16,5); em Alimentos e Bebidas é 14→19, mesma diferença de 5 pontos.

## 6. ML afirma que Premium tem mais exposição — e um praticante discorda

> *"Na teoria, o próprio Mercado Livre alega que o anúncio premium tem mais
> exposição. Isso tá **muito mais atrelado à sua conta, à maturidade da sua conta,
> ao nível de ranqueamento da sua conta** do que propriamente [ao tipo]."*
> — Milton P Rabello, 27/08/2026 (`swCx36qRg0w`)

**O que estava escrito:** nada. Eu tratei a escolha como puramente tarifária.

**Correção:** existe uma alegação de exposição maior no Premium. A leitura de quem
opera é que o efeito real vem da maturidade da conta. Registrar como **hipótese a
testar**, não como fato — e o teste só faz sentido depois que a conta tiver histórico.

## 7. Anúncio de catálogo tem que ser Clássico — e com Full

> *"**Anúncio catálogo tem que ser anúncio clássico.** (…) é um anúncio que tem
> vários vendedores concorrendo por condições, por logística, fato de tá no full ou
> não. **Quem já tem Full liberado tem que entrar em catálogo no Full. É regra
> básica.** (…) se é uma concorrência de preço, eu prefiro ter uma taxa menor para
> ter uma competitividade melhor no meu preço."*
> — Milton P Rabello, 27/08/2026 (`swCx36qRg0w`)

**O que estava escrito:** "Avaliar Catálogo para o cavalo de batalha" — sem dizer
que tipo de anúncio usar.

**Correção:** se entrar em catálogo, é Clássico obrigatoriamente, e com Full.
Catálogo é disputa de preço; 5 pontos de comissão a mais é perder a Buy Box.

## 8. A descrição NÃO alimenta o motor de busca do ML

> *"**Descrição não vai ativar o seu motor de buscas**, então não importa se você
> quiser colocar SEO ali, não vai funcionar, não adianta. Os únicos pontos que vão
> ativar o motor de buscas do Mercado Livre vai ser o **título**, a **ficha
> técnica** e também a parte de **características** (modelo, cor, voltagem)."*
> — diegorojasseller, 12/08/2026 (`KPvPvwmTUC8`)

**O que estava escrito:** "Os três blends saem do título e vão para a ficha técnica
e a descrição, **onde não custam caractere e ainda são indexados**."

**Correção:** a parte "e ainda são indexados" está **errada** para a descrição.
Clássico, Suave e Canela precisam estar na **ficha técnica** (campo Modelo/Linha) —
na descrição servem ao leitor humano, não à busca. A descrição continua valendo
para conversão e para reduzir devolução, não para SEO.

## 9. Quem paga o frete — a divergência está resolvida

> *"Abaixo de dezenove reais, o frete é do comprador. (…) [entre R$ 19 e R$ 79] se
> você oferece frete grátis, **você paga de R$ 6,95 a R$ 8,25**. A partir de setenta
> e nove, **quem oferece o frete grátis é você**, e o custo sobe: **de R$ 13,85 para
> cima**."*
> — Milewa, 25/09/2026 (`7h4R4KPK9bw`)

**O que estava escrito:** divergência entre duas fontes, com instrução de tratar a
segunda leitura como verdadeira até medir.

**Resolvido:** a segunda leitura estava certa. Na faixa R$ 19–78,99 o vendedor paga
o frete grátis, **não** o Mercado Livre. E a estimativa de **R$ 15** usada para os
kits acima de R$ 79 é plausível: o piso citado é R$ 13,85.

## 10. Estoque antigo no Full — os números concretos

> *"Por unidade, o produto pequeno paga menos de um centavo por dia: **21 centavos
> por mês**. Um produto grande, R$ 1,50 por mês. O que pesa é o estoque parado.
> **Depois de quatro meses, a unidade pequena paga mais R$ 1 por mês. Depois de
> seis, R$ 12.**"*
> — Milewa, 25/09/2026 (`7h4R4KPK9bw`)

**Confirma** a armazenagem de R$ 0,007/dia (= R$ 0,21/mês) e dá o que faltava: a
escalada do estoque antigo. Para 100 kits parados, o 5º mês custa +R$ 100 e o 7º,
+R$ 1.200. **É o custo que pune o giro lento, não a armazenagem.**

## 11. Full pode gerar DIFAL e obrigação fiscal em outro estado

> *"No Full, o seu estoque pode ficar num centro **em outro estado**. Isso traz
> notas e obrigações a mais, e **pode ter DIFAL**, conforme o seu regime e os
> estados. Antes de enviar, fale com o seu contador."*
> — Milewa, 25/09/2026 (`7h4R4KPK9bw`)

**O que estava escrito:** nada. Lacuna completa.

**Correção:** entra como pré-requisito do envio ao Full, junto do certificado
digital. A conta já tem **6 anúncios sem dados fiscais** e o certificado vencendo —
o tema fiscal é bloqueador antes de ser detalhe.

## 12. Houve nova mudança de tarifa em 24/08/2026

> *"Vocês viram que agora a partir de **agosto, dia 24**, já tá valendo as **novas
> tarifas de venda** do Mercado Livre. (…) não é um ajuste tão pequenininho assim."*
> — Fica Fácil Assim C/ Everton Duarte, 30/08/2026 (`sXRvihoAh9A`)

**O que estava escrito:** tabela de tarifas com vigência **02/03/2026**.

**Correção:** houve **outra** revisão em 24/08/2026, posterior à que está
documentada. A tabela de custo operacional por peso × faixa de preço pode estar
desatualizada. **Só o simulador da Central do Vendedor vale agora.**

---

## O que segue sem confirmação

| Item | Situação |
|---|---|
| **Limite de 60 caracteres no título** | Nenhum vídeo afirmou o número. Continua vindo de blog — conferir no próprio formulário de cadastro |
| **Variação por sabor em Cápsulas** | Nenhum vídeo tratou de variação em alimento. Segue a confirmar no cadastro |
| **Ciclo de aprendizado de 28 dias** | Não apareceu na varredura. Continua sem fonte primária |
| **Tabela de tarifa pós-24/08/2026** | Sabe-se que mudou; os valores novos, não |

---

## Índice das transcrições

| Data | ID | Canal | Título |
|---|---|---|---|
| 25/09 | `ZCSkvBUUddI` | Seus Produtos Na Internet | ROAS DINÂMICO: a nova função do Mercado Livre Ads |
| 25/09 | `7h4R4KPK9bw` | Milewa | Full vale a pena? Quem paga o frete |
| 22/09 | `upVnEGAYiXc` | Marketfacil | O Mercado Livre mudou o Ads de novo |
| 31/08 | `72nX2ogs8xE` | Bruno Maciel | Product Ads na prática — aula 1 |
| 30/08 | `sXRvihoAh9A` | Fica Fácil Assim | Novas tarifas 2026: cuidado para não vender no prejuízo |
| 29/08 | `LimTOaRTLtY` | Código Shop | Como mantenho meus anúncios em alta |
| 27/08 | `swCx36qRg0w` | Milton P Rabello | Anúncio clássico ou premium? A resposta não é óbvia |
| 27/08 | `0InXzo24tWg` | IC7 ACADEMY BI | Clássico x Premium explicado |
| 25/08 | `BSNDMsezcbc` | Ivan Saldanha | O jeito certo de criar um anúncio |
| 14/08 | `So23jhRR900` | Itamar Rocha | Score do anúncio |
| 12/08 | `KPvPvwmTUC8` | diegorojasseller | Onde colocar as palavras-chave |
| 12/08 | `KvVyJlYt6w0` | Bruno Gontijo | Novos custos para vender em agosto de 2026 |
| 10/08 | `-javeW5ePCg` | Empresa em Ação | Criar anúncio com IA + campanha no Ads |
| 10/08 | `qPVIEY_Fg_E` | Vendedores Mercado Livre BR | Desmistificando Full EP 01 — produtos Estrela |
| 06/08 | `vROtKC6S1yQ` | ViraLucro | Análise de um anúncio de catálogo |
| 04/08 | `JgvBGBYlKAM` | Sidinei_cordeiro | Como montar uma campanha perfeita no Ads |

**Nota sobre a fonte.** Transcrição automática do YouTube erra nome próprio e sigla
— "ROAS" aparece como "Ruas", "ACOS" como "Acos". O sentido se preserva; number e
termo técnico foram conferidos no contexto antes de virar afirmação aqui. E
praticante de YouTube é fonte secundária: melhor que blog de agência, pior que o
simulador da própria conta.
