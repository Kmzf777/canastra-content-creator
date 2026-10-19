# Shopee: estratégia de entrada do 1 kg e do 500 g

> Registro das decisões **aprovadas pelo Rafael**, uma por vez, cada uma com data e fonte.
> Diagnóstico de base: [`02-diagnostico-prontidao-2026-10.md`](02-diagnostico-prontidao-2026-10.md).
> Preços e margens saem de [`scripts/precificar_shopee.py`](scripts/precificar_shopee.py), nunca de
> cabeça. "edu NNNNN" = `https://seller.shopee.com.br/edu/article/NNNNN`.

## Decisões aprovadas

| # | Data | Decisão | Por quê (fonte) |
|---|---|---|---|
| 1 | 15/10/2026 | **Abrir a loja do zero, em CNPJ.** Não existe conta de vendedor da Canastra na Shopee (informado pelo Rafael) | O Full exige CNPJ no Simples, Real ou Presumido, com certificado do mesmo CNPJ (edu 26370). O Vendedor Indicado exige CNPJ (edu 18456). O vendedor CPF paga +R$ 3 por item depois de 450 pedidos em 90 dias (edu 18484): no 1 kg a R$ 99,99, isso tira R$ 3 de um CM3 de R$ 13,50 (script). |
| 2 | 15/10/2026 | **Prazo de preparo (DTS) de 1 dia útil desde o início.** Escolha do Rafael, entre 1 e 2 dias (a minha recomendação era configurar 2 e operar em 1) | O selo de Vendedor Indicado pede preparo de até 1 dia útil e envio no sábado em pelo menos 20% dos casos (edu 18456), então a loja já nasce treinando a métrica. **Risco aceito:** atraso de 5% ou mais, com pelo menos 2 pedidos, vale 1 ponto de penalidade (edu 7955); com 20 pedidos numa semana, 1 atraso basta. 3 pontos no trimestre custam −5% de visibilidade por 14 dias (edu 7955). |

| 3 | 15/10/2026 | **Devolução Fácil: manter no teste grátis de 30 dias** (ele ativa sozinho quando a loja fica elegível) e decidir antes do fim, com os Termos lidos | Custa R$ 0,49 por pedido depois do teste. O teste é único: quem desliga durante os 30 dias não volta (edu 26700). Sem o programa, a devolução é grátis, salvo culpa do vendedor (frete inteiro, mais R$ 15 se ele quiser o produto de volta; edu 23740). **Gatilho:** no dia 25 do teste, comparar o custo das devoluções do período com R$ 0,49 × pedidos e trazer a decisão de manter ou sair. **Termos lidos em 15/10/2026** (edu 27298, de 23/03/2026): o programa cobre o frete de ida (FSF) e o de volta (RSF) **de responsabilidade do vendedor**, até R$ 500 por pedido, para os códigos de motivo que a Shopee define; vale só na logística da Shopee e para pedidos criados durante a inscrição. Os Termos não citam a taxa fixa de R$ 15 do edu 23740. **Ponto de equilíbrio:** com ida + volta de R$ 40 a 60 por devolução culpa do vendedor (*frete do 1 kg não medido*), o programa se paga se mais de ~1% dos pedidos voltarem por culpa nossa (0,49 ÷ 50). |

### Regra de operação que vem com a decisão 2

- **Corte diário:** todo pedido pago até o horário de corte sai no dia útil seguinte, sem exceção. O horário depende da janela de coleta ou do ponto de entrega, que vou ler na Central (passo 6).
- **Teto de volume:** não ligar cupom, campanha nem Ads num volume diário maior do que a expedição despacha em 1 dia. Promoção que gera atraso custa mais que a venda que traz.
- **Semanal:** taxa de atraso e de não envio da semana. Se o atraso passar de 3%, abaixo do gatilho de 5%, o volume para de crescer até a causa ser corrigida. Se a causa for estrutural, o prazo volta para 2 dias, com a sua aprovação.
- **Pendência:** confirmar na Central se o Indicado mede o prazo configurado ou o tempo real de preparo.

## Fase 0: abertura da conta (quem executa: Rafael)

Eu não crio conta, não faço login, não aceito termos e não preencho dados bancários ou fiscais.
Este é o roteiro para você executar. Me avise em cada ✋ para eu ler a tela e conferir.

### Antes de começar, tenha em mãos

| Item | Por quê | Fonte |
|---|---|---|
| Celular com número que a empresa vai manter | O anúncio não aparece para o comprador sem telefone confirmado | edu 13388 |
| E-mail da empresa (não pessoal) | Login e notificações; se a pessoa sair, a loja continua | boa prática |
| Cartão CNPJ (razão social, CNPJ, regime tributário) | Cadastro PJ; o regime precisa ser Simples, Real ou Presumido para o Full | edu 26370 |
| Inscrição estadual e endereço da torrefação (Uberlândia) | Endereço de coleta e emissão de NF-e | edu 18801 |
| Conta bancária PJ do mesmo CNPJ | Saque da Carteira do Vendedor | edu 13388 |
| Certificado digital A1 ou A3 do CNPJ **válido** | O vendedor CNPJ envia todo pedido com NF-e, e a NF-e exige certificado. O mesmo certificado do ML serve; confira a validade (o do ML venceu em 30/09/2026 e foi renovado, `mercadolivre/13-o-que-falta.md`) | edu 18801 |
| Logo da marca em PNG (`marca/`) e nome da loja | Perfil da loja | `marca/LEIA-ME.md` |

### Passo a passo

1. Em `shopee.com.br`, crie a conta Shopee com o telefone e o e-mail da empresa. Uma loja por conta. Até 5 contas por CNPJ são permitidas, mas só em categorias diferentes (edu 16310), então crie **uma loja só**.
2. Em `seller.shopee.com.br`, inicie o cadastro de vendedor e escolha **Pessoa Jurídica / CNPJ**.
3. Preencha os dados da empresa e o endereço de coleta (torrefação). ✋ **Pare antes de aceitar os termos**, leia-os você mesmo e me diga se aparece alguma condição que não está no `02` (por exemplo, taxa de adesão, prazo de repasse ou exigência de categoria).
4. Cadastre a conta bancária PJ.
5. Nome da loja: proponho **"Café Canastra"**, o mesmo nome da marca, porque a busca por marca precisa achar a loja. O nome da loja e o nome de usuário são campos diferentes (edu 16382). ✋ Me mostre as regras de nome e logo antes de salvar (edu 16381).
6. ✋ Assim que a Central abrir, **não cadastre produto ainda**. Me avise para eu ler (só ler):
   - as modalidades de envio disponíveis para o CEP da torrefação (Configurações de Envio);
   - se o Devolução Fácil já aparece ativo (ele ativa sozinho quando a loja é elegível; o teste grátis de 30 dias é único, edu 26700);
   - as opções de emissão de NF-e (ERP integrado, site do governo ou Emissor Shopee, edu 18801);
   - quais formatos de Shopee Ads e de Central de Marketing aparecem para uma loja nova.

Os passos de configuração depois da abertura (prazo de preparo, envio, NF-e, Devolução Fácil e perfil) são decisões e entram aqui uma a uma, com o seu "pode".

## Decisões em aberto (ordem proposta)

1. ~~Prazo de preparo~~ — decidido (nº 2).
2. Emissão de NF-e: Emissor Shopee, ERP ou site do governo (depende do que a Central mostrar no passo 6).
3. ~~Devolução Fácil~~ — decidido (nº 3); revisão no dia 25 do teste.
4. Portfólio inicial: quais SKUs entram, variação ou anúncio separado, kits.
5. Preço por SKU.
6. Tração inicial: vídeo, cupom de seguidor, afiliados.
7. Shopee Ads: quando ligar e com que meta de ROAS.
8. Portões de fase, até Indicado e Full.
