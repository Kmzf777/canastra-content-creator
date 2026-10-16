# Plano — pesquisa de marketplaces

> Spec: `docs/superpowers/specs/2026-10-14-pesquisa-marketplaces-design.md`. Execução por
> workflow (Claude Code), com o material em `pesquisa-marketplaces/`.

## Tarefa 1 — Preparação (feito antes do workflow)
- [x] Pastas `pesquisa-marketplaces/{mercadolivre,shopee,amazon}/{transcricoes,social,observacao}` e `metodo/`
- [x] Ferramentas em `ferramentas/`: `buscar_youtube.py` (busca por data, confere data, frente por
      consulta), `baixar_legendas.py` (legendas pt, retry em 429), `meta_instagram.py` (metadados sem login)
- [x] Teste: busca + legenda de 1 vídeo (429 tratado pela espera de 90 s)

## Tarefa 2 — Workflow (fases)
1. **Método** ‖ **Coleta YouTube ML → Shopee → Amazon** (sequencial) ‖ **Navegador** (série)
2. Por plataforma, assim que a coleta dela termina: **8 analistas → verificador** (pipeline)
3. **Transcrição social** (série, depois do navegador) → **social** por plataforma
4. **Consolidação** por plataforma (precisa das 8 notas + social) → **crítico de completude**

Cada agente devolve um resumo estruturado (arquivos escritos, nº de fontes por camada,
afirmações-chave) para o relatório final.

## Tarefa 3 — Fechamento
- [ ] Conferir arquivos (contagem, notas vazias, frentes sem fonte oficial)
- [ ] `pesquisa-marketplaces/LEIA-ME.md` (índice, como reproduzir, limites)
- [ ] Marcar a rodada v1 (`mercadolivre/16-…`, `shopee/`, `amazon/`) como enviesada no LEIA-ME
- [ ] Commit só de `pesquisa-marketplaces/` e destes dois documentos
