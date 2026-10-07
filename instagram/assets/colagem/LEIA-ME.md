# Biblioteca de colagem

Peças prontas para motion de colagem do Café Canastra. **Toda peça gerada ou
recortada para um motion entra aqui antes de entrar no projeto** — assim a
próxima peça começa com o acervo da anterior.

## Como achar

```bash
python -m uv run python scripts/biblioteca_colagem.py buscar cereja vermelha
python -m uv run python scripts/biblioteca_colagem.py listar fruto
```

A busca casa todas as palavras contra id, categoria, tags e nota. O índice é
`indice.json` (versionado); os PNG não são versionados, como em `../embalagem/`.

## Como usar num projeto

```bash
python -m uv run python scripts/biblioteca_colagem.py publicar <projeto> <id> [<id> ...]
```

Copia as variantes para `instagram/remotion/projetos/<projeto>/public/colagem/<nome>-bN.png`,
que é o caminho que `src/colagem/pecas.tsx` lê, e anota o projeto em `usado_em`.

## Nome dos arquivos

```
brutos/AAAA-MM-DD_<assunto>.png                      folha original (ChatGPT) — a fonte
pecas/<categoria>/AAAA-MM-DD_<nome>-b0|b1|b2.png      peça processada, 3 bordas para o boil
```

A data é a da **geração**, não a do uso. `b0/b1/b2` são a mesma peça com borda de
papel recortado diferente; o Remotion alterna entre elas a cada 3 quadros.

## Categorias

| categoria | o que entra |
|---|---|
| `xicara-utensilio` | xícara, colher de prova, prato de balança, peneira |
| `grao` | grão verde, torrado, defeituoso |
| `fruto` | cereja de café em qualquer estágio, cacho |
| `planta` | pé de café, folha, muda |
| `foto-real` | foto da base verificada impressa com borda rasgada |
| `textura` | kraft, milimetrado |
| `fita` | fita crepe, adesivo |
| `grafismo` | seta, rabisco, círculo, sublinhado |
| `papelaria` | tachinha, clipe, post-it, etiqueta de barbante |

## Regras que não mudam aqui

- **Embalagem não entra nesta biblioteca.** Pacote vem só do recorte com laudo
  (`../embalagem/`, publicado por `instagram/recorte/publicar.py`).
- `origem` é `gerado-chatgpt`, `real-verificada` ou `codigo`. Foto real só de
  `base-curada/01-real-verificada` (ou `02` com a ressalva do CLAUDE.md); nunca de
  `03-mood-terceiros`, `04-quarentena` nem `raspagem/`.
- Nenhuma peça com rosto de pessoa real sintetizado, nem texto gerado por modelo.
- Gerado sobre **branco liso** e recortado local por `scripts/colagem_assets.py`
  (lição 49 do CLAUDE.md).
