---
name: canastra-ml-anuncio
description: Use when creating or configuring a Café Canastra listing on Mercado Livre — title, ficha técnica, photos, description, listing type (Clássico/Premium), shipping, wholesale tiers, availability time, kits. A field-by-field checklist; the browser mechanics live in canastra-mercadolivre.
---

# Criar e configurar anúncio

A mecânica do painel (clique triplo, acordeão, conferir na lista) está em
**`canastra-mercadolivre`** — carregue as duas. Preço vem de **`canastra-ml-precificacao`**.

**Nada é criado nem editado sem o OK do Rafael, campo a campo.** Anúncio novo nasce
**pausado**; quem ativa é ele.

## Checklist por campo

| Campo | Regra |
|---|---|
| **Título** | ≤ **60** caracteres (o formulário mostra `60 / 60`). Termos que o comprador busca primeiro: formato (`Em Grãos`/`Moído`), `Especial`, torra, peso, região. Não mexa no título de anúncio que já vende |
| **Categoria** | Alimentos e Bebidas › Mercearia › Infusões › Café › Café Moído e em Grão |
| **Ficha** | É indexada (a descrição **não**). Valor limpo, sem palavra-chave enfiada: Marca `Café Canastra`, Linha, Modelo (`Suave`/`Clássico`), Formato do café, Tipo `100% arábica`, Nível de torrado (`Médio`/`Escura`), Peso, Formato de venda (`Unidade`/`Kit` + unidades), Livre de TACC, Validade. O ML normaliza alguns valores (`Cafe Canastra`) — não redigite |
| **EAN** | Do verso real do pacote. ⚠ `7892262780089` está repetido no Clássico 500 g moído e grãos |
| **Fotos** | Uma por chamada do `file_upload`. Capa = posição 1. Só pixel real da embalagem (skill `canastra-embalagem`); nunca rascunho de lateral/verso. ≥ 1200 px |
| **Vídeo** | Os líderes têm; o ML cobra como objetivo pendente |
| **Descrição** | Bloco de origem (região, variedade, altitude, pontuação) → perfil sensorial → para quem → frescor → o que vem na caixa. **Sem link, telefone, e-mail ou WhatsApp.** Textos prontos em `mercadolivre/textos/` |
| **Tipo** | < R$ 150 → Clássico; ≥ R$ 150 → Premium (parcelamento) |
| **Frete** | Grátis obrigatório ≥ R$ 79. Leia o custo ao lado da opção e **pare se fugir do previsto** |
| **Embalagem de envio** | O ML calcula (29 × 27 × 11 cm, 1,128 kg no 1 kg) e pede conferência. Medida real pode baixar o frete |
| **Prazo de disponibilidade** | Torra sob demanda → preencha os dias reais. Atraso de envio é o que derrubou a reputação |
| **Atacado** | Só CNPJ vê; até 5 faixas; **teto = preço − economia de frete/un** (balão do ícone vermelho) |
| **Estoque / SKU** | Estoque real; SKU da tabela (Suave `07`, Clássico `08`, kits `08-K2`) |

## Depois de gravar

1. Toast de sucesso **não é prova**. Confira na lista
   (`vendedores.mercadolivre.com.br/anuncios/lista?search=<id>`) e na página pública.
2. Registre a alteração na tabela **"Alterações aplicadas"** do `mercadolivre/LEIA-ME.md`,
   com data, ID, o que mudou e "Rafael, na conversa".
