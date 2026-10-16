---
name: canastra-conteudo
description: Use when producing or auditing any Café Canastra image — packshot de catálogo, troca de fundo, composição de cena, UGC, post de rede social — or when an image came back from ChatGPT and needs to be approved, corrected or saved into the repo.
---

# Hub de conteúdo — Café Canastra

Todo conteúdo de imagem deste projeto passa pelo mesmo fluxo de cinco fases. O que
muda entre um packshot e uma cena de fazenda é **o que entra na fase 1 e como se
escreve a fase 2** — a mecânica e o rigor das fases 3 a 5 são idênticos.

## Rotear primeiro

| A imagem tem… | Subskill | O que ela garante |
|---|---|---|
| embalagem legível no quadro | **canastra-embalagem** | rótulo correto letra por letra |
| cenário, mesa, lavoura, pessoas, UGC | **canastra-cena** | realismo e procedência das referências |
| ambos (UGC com o pacote na mão) | as duas, nessa ordem | embalagem manda no rótulo, cena manda no resto |

Se a embalagem aparece e dá para ler, **canastra-embalagem não é opcional** — é ela
que evita publicar um sósia da marca.

## As cinco fases

1. **Curadoria** — escolher quais arquivos podem virar pixel. Cada subskill diz de onde.
2. **Prompt** — blocos obrigatórios da subskill + o que é específico daquela imagem.
3. **Geração** — Claude in Chrome → ChatGPT. Mecânica abaixo.
4. **Conferência ampliada** — a fase que mais falha. Regras abaixo.
5. **Registro** — salvar no destino certo e gravar a lição.

---

## Fase 4 — conferência: a regra que mais se perde

**Você só pode marcar um campo como conferido se a fonte de referência permitir
lê-lo.** Se o número está ilegível na foto, o campo não está certo nem errado: está
**não verificável**. Escreva isso, com todas as letras, e pare.

Um agente testado neste repositório aprovou uma lateral de cápsula dizendo que as
quatro notas sensoriais "batem com a foto real". Duas delas — AROMA e DOÇURA — são
fisicamente ilegíveis na referência: a barra vai 100% cheia e o número fica preto
sobre preto. Ele viu `10` na imagem gerada, viu preto na referência, e converteu
"não consigo ler" em "confere". O valor real era de fato 10, e ainda assim o
veredito era inválido: foi sorte, não conferência. Na rodada anterior o mesmo campo
tinha saído `70 / 80 / 80 / 40` e passaria pelo mesmo raciocínio.

### Como conferir de verdade

- **Nunca julgue pela imagem inteira.** Em miniatura, erro de letra some. Recorte a
  faixa de texto e amplie com PIL antes de opinar:
  ```python
  c = Image.open(gerada).crop((x0, y0, x1, y1))
  c.resize((c.width*4, c.height*4), Image.LANCZOS).save(destino)
  ```
- **Amplie a referência também**, no mesmo trecho. Conferência é comparação entre
  dois recortes, não entre um recorte e a sua memória.
- **QR e código de barras gerados estão sempre errados.** O modelo redesenha o
  padrão. Não chame isso de "decorativo" nem de "equivalente": reporte como
  `regenerado — não escaneável`. O que fazer com o achado:
  - packshot de catálogo → **não reprova**, mas entra como ressalva escrita no
    veredito. É característica do fluxo, não defeito daquela imagem;
  - qualquer peça onde alguém vá apontar a câmera (embalagem real, PDV, impresso)
    → **reprova** até compor o código real por cima.
- **Reporte por campo**, não em bloco. `✓ confere` / `✗ errado: saiu X, é Y` /
  `? não verificável na referência`.

### Tabela de racionalizações

| Desculpa | Realidade |
|---|---|
| "No geral está certo, aprovo" | "No geral" não é unidade de conferência. Campo a campo. |
| "A barra cheia bate com a referência" | Barra cheia esconde o número. Isso é ausência de leitura, não leitura. |
| "O QR é decorativo, nem conto no veredito" | Decorativo ou não, é um código. Pode não reprovar um packshot — mas some do veredito só se você o escrever como ressalva. |
| "O cliente está esperando" | Uma embalagem errada impressa custa mais que uma rodada de conferência. |
| "20 de 21 já passaram, esse é igual" | Os erros desta sessão apareceram justamente no último. |
| "Já ampliei uma parte, o resto deve estar ok" | Os erros são locais: `EXPRESSO`, `CATUAI`, `7,0→70`. Ampliar uma parte não cobre outra. |

### Bandeiras vermelhas — pare e volte à fase 4

- Você escreveu "confere" sem ter aberto um recorte ampliado daquele campo.
- Você não consegue apontar em qual pixel da referência leu o valor.
- Você está prestes a aprovar um QR ou código de barras gerado.
- Você está com pressa e o texto é denso.

**Se a referência não permite ler, a saída não é chutar nem "copiar da foto" — é
perguntar ao Arthur e soletrar o valor no prompt.** Ver `canastra-embalagem`.

---

## Fase 3 — mecânica do ChatGPT via Claude in Chrome

Medido nesta sessão, em conta Plus com interface em português.

| Passo | O que funciona |
|---|---|
| Aba | `tabs_create_mcp` sempre nova; nunca reaproveitar tabId de outro fluxo |
| Composer | seletor `.ProseMirror` — o antigo `#prompt-textarea` sumiu |
| Anexar | `find` o input "Anexar arquivos" e `file_upload` com **todos os caminhos numa chamada só**, na ordem que o prompt cita como FIRST/SECOND |
| Fechar o overlay do upload | **`Escape`**. O X fica em cima do botão de *chat temporário*: clicar ali recarrega em `?temporary-chat=true` e leva anexos e prompt junto |
| Inserir prompt | `document.execCommand('insertText', false, txt)`; **nunca** `computer.type` (o `\n` envia antes da hora) |
| Conferir inserção | comparar `el.textContent.length` com o tamanho esperado; a diferença normal é 2 por quebra de parágrafo |
| Enviar | `find` no botão Enviar e clicar; **se o composer continuar cheio, clique de novo** — o primeiro clique costuma só focar |
| Enviar (fallback) | screenshot e clique na coordenada real do botão; a ref do `find` envelhece |
| Confirmar envio | `location.pathname` mudou de `/` para `/c/...` **e** composer zerou |
| Esperar | blocos de `wait` de 10s; um poll longo em JS estoura o timeout de 45s do CDP |
| Achar a imagem | `img[alt]` casando `/gerada|Generated/` — o alt é `Imagem 1 gerada`, não `Imagem gerada` |
| Baixar | clicar na imagem para abrir tela cheia, depois `find` no botão **Baixar**. O ícone ⬇ inline não baixa de forma confiável |

### Cena aprovada não se arrisca em follow-up

**Follow-up de edição no mesmo chat não preserva a imagem — regenera.** Medido em
05/10/2026 no post da cozinha: a v1 voltou com a cena certa e só o selo circular
errado. O follow-up nomeava a operação e repetia o que preservar ("same kitchen,
same counter, same light, same package position"). A v2 veio com **outra cozinha
inteira**. `np.abs(v1-v2).max(axis=2) > 12` deu **79,2% dos pixels alterados**,
para um pedido que cobria ~1,1% do quadro.

A documentação da OpenAI prescreve *"small, single-change follow-ups"*. Na nossa
medição ela não se cumpre. Então:

- deu certo a cena e errou um detalhe → **salve o arquivo** e conserte por
  composição local (degrau 6) ou numa **conversa nova**;
- nunca peça "só isso" por cima de um resultado que você já quer manter;
- gerar várias imagens na mesma conversa tem o mesmo risco — ver
  `docs/PESQUISA-REALISMO-GERACAO.md` §2.

### Salvar

```bash
python -m uv run python scripts/_pega_download.py "<destino relativo>"
```

Ele pega o PNG **mais recente** de Downloads — sem filtrar por nome, porque o ChatGPT
já nomeou o arquivo de três jeitos (`ChatGPT Image*`, `Imagem do ChatGPT*` e, desde
04/10/2026, o **título do chat**) — e imprime origem, destino e dimensões. Cada arquivo
de origem só pode ser consumido uma vez: se o clique em Baixar não disparar, o script
aborta em vez de regravar o download anterior.

**Paralelizar: gere em paralelo, baixe em série.** Vários agentes baixando ao mesmo
tempo trocam as imagens entre si sem erro nenhum. E o ChatGPT **compartilha o rascunho
e os anexos do composer entre abas** — leia o `.ProseMirror` e a lista de anexos
imediatamente antes de cada envio.

**Confira o carimbo de hora do arquivo de origem que ele imprimiu.** O script já
salvou silenciosamente uma imagem do dia anterior porque procurava só um dos dois
padrões de nome (`ChatGPT Image*` em inglês, `Imagem do ChatGPT*` em português) e
as dimensões eram idênticas. Dimensão igual não prova que é a imagem certa.

### Alternativa: Grok Imagine (grok.com/imagine)

Usado a pedido do cliente em 07/10/2026, nos slides 3, 7, 8 e 9 do carrossel de
história. Conta "Rafael Café Canastra", interface em português.

| Passo | O que funciona |
|---|---|
| Imagem nova | navegue para `/imagine` a cada imagem. A caixa de baixo de um post (`Descreva sua edição`) **edita aquela imagem**, não cria outra |
| Anexar | o único `input[type=file]` com `multiple` é o do formulário do prompt (`find` "file type button inside the prompt form"). Use `file_upload` com **todos os caminhos numa chamada**, na ordem FIRST/SECOND. Aceitou 4; as miniaturas aparecem na ordem enviada |
| Proporção | **com anexo, volta para "Automático"**, que herda a proporção da primeira fonte. Reabra o seletor e escolha `2:3 Pôster` toda vez. Não há 4:5 nem 3:4 |
| Prompt | é um tiptap/ProseMirror: use `execCommand('insertText')` e confira o comprimento, como no ChatGPT |
| Enviar | seta azul. A URL vira `/imagine/post/<id>`, e **o id muda quando a imagem termina**: releia `location.pathname` antes de baixar |
| Baixar | `find` "Baixar button for the main image (bottom action bar)". O arquivo cai como `grok-image-<id>.jpg` |
| Salvar | **copie pelo id**, nunca pelo mais recente. `_pega_download.py` procura PNG e pegaria o download de outra sessão (lição 51) |
| Resolução | sai **832×1248**. Não há versão maior no post; amplie na montagem, sem outro passe |
| 1ª vez | modal **"Ano de Nascimento"**, irreversível. É dado pessoal: pare e peça ao usuário. Cookies opcionais: `Rejeitar todos` |

O rótulo se comporta como no ChatGPT: logo, selo, `250g` e `SPECIALTY / ESPECIAL / SCA
80+` saíram certos; `Desde 1985` e a linha `TORRADO E MOÍDO` quebraram toda vez. Componha
com `scripts/compor_rotulo.py --preset classico-moido|suave-moido|canela-moido`. Com os
três pacotes no mesmo quadro, passe `--regiao` de cada um: a logo é igual nos três, e o
alinhamento pode casar com o pacote vizinho.

---

## Fase 5 — registro

- Saída de catálogo vai em `saida-teste/catalogo-estudio/<N>-<slug>/` (gitignored).
- Prompt novo ou convenção nova: edite `scripts/prompts_catalogo.py` e rode.
  **Nunca edite `docs/PROMPTS-ESTUDIO-CATALOGO.md` à mão** — ele é sobrescrito.
- Erro que custou uma rodada vira lição no `Registro de lições` do `CLAUDE.md`,
  no formato **sintoma → causa raiz → regra**. Erro não registrado se repete na
  próxima sessão, que não tem a memória desta.

## Regras da marca que nenhuma fase derruba

- **A embalagem entra como pixel, nunca como texto solto.** Descrever o logotipo e
  deixar o modelo desenhar produz um sósia.
- **Rosto de pessoa real nunca é sintetizado.** Foto de pessoa é foto.
