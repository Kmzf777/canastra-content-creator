# Agentes de marketplace: a estratégia (19/10/2026)

> Síntese de 5 frentes de pesquisa, em `agentes-ia/`: `reddit-foruns/`, `github-ferramentas/`,
> `youtube/` (35 vídeos lidos), `social/` (TikTok e Instagram, 27 transcrições) e `metodo-producao/`.
> A pergunta era como quem faz de verdade monta agentes que gerem contas de marketplace, de um jeito
> que sirva para qualquer marketplace. Os números de resultado que aparecem nas fontes são quase todos
> autodeclarados por quem vende ferramenta. O método é o que se repete entre as fontes.

## 1. O que a pesquisa decidiu (e a fonte de cada ponto)

1. **Ninguém monta "um agente que faz tudo", e quase ninguém divide por canal.** A divisão é por
   **função**: saúde da conta, preço, anúncio, ads, estoque, atendimento, concorrência, relatório.
   Cada função lê a mesma base de fatos (custos, metas, regras da marca). Quando há canais, quase
   sempre é um assistente com **um conector por canal** (Hunter, tiops, DataDoe, Sophie, Profasee,
   Ad Badger; reddit-foruns §a2; social §a1).
2. **A autonomia sobe em 3 degraus:**
   - observar e recomendar;
   - aprovar cada ação, com o antes e o depois;
   - automático, mas só nas ações baratas de desfazer e dentro de limites numéricos.

   Até agência com mais de 200 marcas ainda não deixa o agente publicar (Trivium, EF-gbTLBvYM 05:36;
   Profasee h0lj3AM6T7Y 04:10).
3. **A trava é medida pelo estrago:** "quanto dinheiro sai se isso estiver errado por 24 h". Negativar
   termo e pausar o que não vende podem ser automáticos. Subir lance, verba ou preço passa sempre por
   aprovação (reddit-foruns §a3).
4. **A conta fica num script, e o LLM só lê e resume.** Preço, margem e reposição saem de código com
   piso. Nas lojas tocadas por agente (Project Vend), o agente vendeu abaixo do custo e deu desconto a
   quem pediu (metodo-producao §b; Ad Badger hNrLVm0NPAU 20:40).
5. **Memória é o que separa agente útil de agente perigoso:**
   - registro do que já mudou, senão ele mexe de novo no mesmo lance;
   - contexto da marca: o termo em que se investe de propósito, a margem, o estoque;
   - quando você recusa uma proposta, o motivo vira regra gravada.

   Fontes: zQBEfxPQdbo 04:39; EF-gbTLBvYM 00:00.
6. **Os dados vêm da API oficial, guardados num histórico próprio.** Consultar ao vivo a cada pergunta
   esbarra em limite e em dado que some, porque algumas APIs só guardam 60 dias. Quem usa navegador
   usa para ler, e mesmo assim desaconselha: no navegador o agente alcança as configurações da conta
   (3iVMaqvzW9E 05:46).
7. **As plataformas fecharam o navegador para agentes:**
   - **Mercado Livre, cláusula 12 dos Termos (modificados em 15/10/2026, lida por mim na página):**
     proíbe "agentes ou qualquer outro software ou serviço, inclusive os baseados em inteligência
     artificial, que atuem de forma autônoma ou semiautônoma" para "acessar, interagir, executar
     operações [...] por conta própria ou de terceiros, sem a correspondente autorização expressa do
     Mercado Livre", em especial (b) "informações ou funcionalidades que estejam disponíveis apenas
     mediante autenticação prévia". **O #mercadolivre lendo o painel pelo Chrome cai nisso.** A API
     com app registrado é o acesso autorizado.
   - **Amazon:** desde 04/03/2026 o contrato do vendedor tem uma política de agentes. O agente se
     identifica e para quando a Amazon pede. Há relato de bloqueio ativo de agente de navegador. Não li
     o texto oficial, porque ele exige login.
   - **Shopee e TikTok Shop:** não achei a regra. O caminho seguro é o mesmo, a API oficial.
8. **Conectores oficiais em 2026:**
   - **Amazon:** Ads MCP (beta aberto) e Selling Partner plugin para o Claude (23/09/2026, só EUA, sem
     ads e sem custo do produto).
   - **Mercado Livre:** MCP só de documentação.
   - **Bling:** MCP com escrita confirmada (05/10/2026).
   - **Shopee e TikTok:** nenhum conector oficial.

   Fonte: github-ferramentas §a.
9. **O que funciona e o que derrapa:**
   - Funciona: resumir, achar gasto sem venda, auditar anúncio e alertar estoque.
   - Derrapa: mandar. Num relato, o agente propôs cortar um termo que trazia 30% das conversões
     (reddit-foruns §a6).
   - O que mais quebra é manutenção: token expirado, relatório que muda de formato.
10. **Avaliação com números.** Separe de 20 a 50 casos por canal e meça quanto você aprova sem editar.
    Acima de 90%, dá para afrouxar a revisão; abaixo de 70%, o prompt precisa mudar
    (metodo-producao §a10).

## 2. O molde (vale para qualquer marketplace)

Um agente de marketplace é sempre a mesma máquina. Muda só o **conector** e as **regras do canal**.

```
                ┌──────────── Rafael no Discord (#mercadolivre, #amazon, #shopee, #tiktokshop)
                │   cartões de aprovação · relatório da manhã · /calculadora
                ▼
  ┌─────────── AGENTE DO CANAL (mesmo código, config por canal) ───────────┐
  │  rotina fixa (código): coleta → compara com limites → alerta/propõe    │
  │  diagnóstico aberto (LLM): só quando o Rafael pergunta                 │
  │  skills por FUNÇÃO (iguais em todo canal, parametrizadas):             │
  │   saúde · preço/margem · anúncio · ads · estoque · atendimento ·       │
  │   concorrência · relatório                                             │
  └──────────┬──────────────────────────────┬──────────────────────────────┘
             │ lê/escreve                   │ lê
     CONECTOR do canal               BASE DE FATOS (uma só, no repositório)
     (API oficial; Chrome só          custos.md com o CMV de TODOS os produtos,
      onde não houver API e a         metas e limites por canal, regras da marca,
      plataforma permitir)            registro de decisões, snapshots diários
```

### 2.1 Os 5 componentes

| Componente | O que é | Regra |
|---|---|---|
| **Conector** | o acesso aos dados do canal | API oficial primeiro. Snapshot diário guardado em arquivo (histórico próprio). Navegador só para ler, só onde não há API e a plataforma não proíbe; captcha é parada obrigatória |
| **Base de fatos** | `custos.md` (CMV de 1 kg, 500 g, 250 g, drip, cápsula e kits), `limites.json` por canal, regras da marca | uma fonte só; o agente nunca usa número que não esteja aqui ou no script |
| **Skills por função** | saúde, preço e margem, anúncio, ads, estoque, atendimento, concorrência, relatório | a mesma skill serve a todos os canais; o que muda vem da config do canal |
| **Scripts** | `precificar_<canal>.py`, piso de preço, reposição, curva ABC por lucro | toda conta passa por script; preço sem script validando não vai para a proposta |
| **Fila de aprovação e registro** | cartão no Discord: campo, valor atual, valor proposto, por quê e estrago se der errado. Botões Aprovar e Recusar (com motivo) | aprovado é executado e conferido na conta; recusado vira regra em `limites.json`; tudo vai para `decisoes.jsonl` |

### 2.2 Tabela de risco (decide o degrau de cada ação)

| Ação | Estrago em 24 h se errar | Degrau hoje | Pode virar automático? |
|---|---|---|---|
| Ler painel, pedidos, métricas e concorrência | nenhum | automático | já é |
| Relatório e alertas | nenhum | automático | já é |
| Rascunho de resposta a pergunta | baixo | aprovar | sim, se responder só com o que está no anúncio e passar de 90% de aprovação |
| Negativar termo ou pausar anúncio pago sem venda | baixo | aprovar | sim, com regra (ex.: 25 cliques sem venda) |
| Texto, título, atributos e fotos | médio, reversível | aprovar | não |
| Preço e promoção | alto | aprovar, e só com piso do script | não |
| Verba, lance para cima, campanha nova | alto | aprovar, com teto diário | não |
| Envio de estoque (Full, FBA), reativar ou excluir anúncio, contratos | alto e irreversível | nunca: o agente prepara o passo a passo | não |

### 2.3 A rotina (imita o gestor humano)

- **Todo dia, 7h, sem LLM na coleta:** pedidos atrasados, perguntas sem resposta, reputação e métricas
  de saúde, ruptura de estoque, gasto de ads sem venda. Sai uma lista curta no canal. Se nada quebrou,
  ele diz isso em uma linha.
- **Toda semana:** auditoria dos anúncios comparada com a semana anterior, termos de ads, preço de
  concorrentes e propostas da semana, cada uma num cartão.
- **Todo mês:** CM1, CM2 e CM3 por SKU e canal, curva ABC por lucro, revisão de preço e de limites.
- **Sob demanda:** conversa no canal, como hoje.

## 3. Como fica para cada canal da Canastra

| Canal | Conector recomendado | O que muda | Primeira coisa a fazer |
|---|---|---|---|
| **Mercado Livre** | **API oficial** com app próprio no DevCenter (OAuth, refresh token) | sai o Chrome lendo o painel, pela cláusula 12. Alguns dados só existem no painel (o filtro de "experiência de compra"); para esses, pedir autorização ao ML ou ler à mão | criar o app no DevCenter; o agente passa a ler pela API |
| **Amazon** | **SP-API e Ads API** (cadastro de desenvolvedor) ou, quando chegar ao Brasil, o plugin oficial Selling Partner | o Seller Central pelo Chrome tem risco pela política de agentes | pedir o acesso de desenvolvedor à SP-API (pode ser recusado e demora) |
| **Shopee** | **Open Platform** (app de parceiro) | conta ainda não existe (greenfield) | abrir a conta e o app de parceiro juntos |
| **TikTok Shop** | **TikTok Shop Partner API** | a loja existe, sem produto | cadastrar produtos; API depois que houver venda |

Enquanto a API de um canal não estiver pronta, o agente desse canal fica no **degrau 0**. Ele trabalha
com o que você manda (print, CSV exportado por você) e com a pesquisa. É o método mais simples que
apareceu (PXq43owGJ6g: relatório baixado à mão e uma skill que o analisa).

## 4. O que já temos e o que falta

| Peça | Hoje | Falta |
|---|---|---|
| Agente no Discord | só o `#mercadolivre` (conversa, lê pelo Chrome) | agente genérico `AgenteMarketplace` (mesmo código para os 4) com `#amazon`, `#shopee`, `#tiktokshop` |
| Base de fatos | `custos.md` só com 1 kg, 500 g e kits | CMV de todos os produtos; `limites.json` por canal; `decisoes.jsonl` |
| Scripts | precificar de ML, Amazon, Shopee e TikTok | piso de preço como trava (hook), curva ABC por lucro, reposição |
| Calculadoras | 4 guias publicados | comando `/calculadora` que posta o link; CMV editável na página |
| Aprovação | o agente pergunta no texto | cartão com botões no Discord, como o CRM já faz |
| Rotina | nenhuma | relatório das 7h e semanal |
| Conectores | Chrome no ML | API do ML primeiro; depois SP-API |

## 5. Ordem proposta

1. **Base de fatos e calculadoras** (sem risco, serve a tudo): CMV de todos os produtos em
   `custos.md`, CMV editável nas 4 calculadoras e `/calculadora` no Discord.
2. **Agente genérico de marketplace** no bot: o `#mercadolivre` vira uma instância. Entram `#amazon`,
   `#shopee` e `#tiktokshop` no degrau 0, sem conector e só conversa, com skills por função e cartões
   de aprovação.
3. **Conector do ML pela API oficial** (app no DevCenter). O Chrome para de ler o painel do ML.
4. **Rotina das 7h e semanal no ML**, só leitura e alertas. Mede a taxa de aprovação sem edição.
5. **Amazon pela SP-API** (o pedido de acesso pode levar semanas, então começar o pedido já).
6. **Shopee e TikTok** quando houver conta ou venda.
7. **Afrouxar degraus** só com números: ação com mais de 90% de aprovação sem edição em 30 casos pode
   subir de degrau.

## 6. Decisões do Rafael

1. **ML pela API:** criar o app no DevCenter e tirar o Chrome do painel do ML. A alternativa é pedir
   ao ML a "autorização expressa" para assistente de IA no navegador, ou manter e aceitar o risco.
2. **Amazon:** pedir agora o acesso de desenvolvedor à SP-API, ou esperar o plugin oficial chegar ao
   Brasil.
3. **Um agente por canal (o mesmo código) com skills por função:** confirmar esse desenho.
4. **Degrau inicial:** "aprovar cada ação" em todos os canais, com a tabela de risco da seção 2.2.
5. **Relatório das 7h:** em qual canal e em qual horário.

## 7. Lacunas

- Texto oficial da política de agentes da Amazon e se vale para a Amazon.com.br.
- Regra da Shopee e do TikTok Shop sobre automação.
- Como o ML concede a "autorização expressa" da cláusula 12, e por qual canal.
- Caso brasileiro com números de agente operando conta no ML ou na Shopee (não há publicado).
