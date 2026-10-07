"""Biblioteca de peças de colagem do Café Canastra.

Cada peça entra uma vez, com data, categoria, tags e procedência, e fica
reutilizável por qualquer motion. O índice (`indice.json`) é versionado; os PNG
não (mesma convenção de `instagram/assets/embalagem/`).

    instagram/assets/colagem/
      indice.json                       <- a busca lê isto
      brutos/AAAA-MM-DD_<folha>.png      folha original do ChatGPT / foto real
      pecas/<categoria>/AAAA-MM-DD_<nome>-b0.png   (b0/b1/b2 = bordas do boil)

Uso:
    python -m uv run python scripts/biblioteca_colagem.py buscar cereja vermelha
    python -m uv run python scripts/biblioteca_colagem.py listar [categoria]
    python -m uv run python scripts/biblioteca_colagem.py publicar 06-voce-sabia-especial <id> [<id> ...]

`publicar` copia as variantes para `projetos/<p>/public/colagem/<nome>-bN.png`,
o caminho que os componentes Remotion leem, e anota o uso no índice.
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import date
from pathlib import Path

from PIL import Image

RAIZ = Path("instagram/assets/colagem")
INDICE = RAIZ / "indice.json"
PROJETOS = Path("instagram/remotion/projetos")

CATEGORIAS = {
    "xicara-utensilio": "xícara, colher, prato de balança, peneira, utensílio de café",
    "grao": "grão verde, torrado, defeituoso, punhado",
    "fruto": "cereja de café em qualquer estágio, cacho",
    "planta": "pé de café, folha, muda",
    "foto-real": "foto real da base verificada, impressa com borda rasgada",
    "textura": "papel kraft, milimetrado, fundo",
    "fita": "fita crepe, adesivo",
    "grafismo": "seta, rabisco, círculo, sublinhado, carimbo desenhado",
    "papelaria": "tachinha, clipe, post-it, etiqueta de barbante",
}
ORIGENS = {"gerado-chatgpt", "real-verificada", "codigo"}


def carregar() -> list[dict]:
    if not INDICE.exists():
        return []
    return json.loads(INDICE.read_text(encoding="utf-8"))


def salvar(itens: list[dict]) -> None:
    RAIZ.mkdir(parents=True, exist_ok=True)
    itens.sort(key=lambda i: (i["categoria"], i["id"]))
    INDICE.write_text(json.dumps(itens, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def registrar(nome: str, categoria: str, variantes: list[Path], tags: list[str], origem: str,
              bruto: str | None = None, prompt: str | None = None, dia: str | None = None,
              nota: str = "") -> dict:
    """Copia as variantes para a biblioteca e grava/atualiza a entrada no índice."""
    if categoria not in CATEGORIAS:
        raise SystemExit(f"categoria '{categoria}' não existe: {sorted(CATEGORIAS)}")
    if origem not in ORIGENS:
        raise SystemExit(f"origem '{origem}' não existe: {sorted(ORIGENS)}")
    dia = dia or date.today().isoformat()
    ident = f"{dia}_{nome}"
    destino = RAIZ / "pecas" / categoria
    destino.mkdir(parents=True, exist_ok=True)
    arquivos = []
    for i, v in enumerate(variantes):
        alvo = destino / (f"{ident}-b{i}.png" if len(variantes) > 1 else f"{ident}.png")
        shutil.copy2(v, alvo)
        arquivos.append(alvo.as_posix())
    w, h = Image.open(arquivos[0]).size
    entrada = {
        "id": ident, "nome": nome, "categoria": categoria, "data": dia,
        "tags": sorted(set(t.lower() for t in tags)), "origem": origem,
        "arquivos": arquivos, "dimensoes": [w, h], "bruto": bruto, "prompt": prompt,
        "usado_em": [], "nota": nota,
    }
    itens = [i for i in carregar() if i["id"] != ident]
    antigo = next((i for i in carregar() if i["id"] == ident), None)
    if antigo:
        entrada["usado_em"] = antigo.get("usado_em", [])
    itens.append(entrada)
    salvar(itens)
    return entrada


def buscar(termos: list[str]) -> list[dict]:
    t = [x.lower() for x in termos]
    def casa(i: dict) -> bool:
        texto = " ".join([i["id"], i["categoria"], i.get("nota", ""), *i["tags"]]).lower()
        return all(x in texto for x in t)
    return [i for i in carregar() if casa(i)]


def publicar(projeto: str, ids: list[str]) -> None:
    pasta = PROJETOS / projeto / "public" / "colagem"
    pasta.mkdir(parents=True, exist_ok=True)
    itens = carregar()
    por_id = {i["id"]: i for i in itens}
    for ident in ids:
        if ident not in por_id:
            raise SystemExit(f"id '{ident}' não está no índice")
        it = por_id[ident]
        for k, arq in enumerate(it["arquivos"]):
            alvo = pasta / (f"{it['nome']}-b{k}.png" if len(it["arquivos"]) > 1 else f"{it['nome']}.png")
            shutil.copy2(arq, alvo)
        if projeto not in it["usado_em"]:
            it["usado_em"].append(projeto)
        print(f"publicado {ident} -> {pasta.as_posix()}/{it['nome']}-b*.png")
    salvar(itens)


def _linha(i: dict) -> str:
    uso = ",".join(i["usado_em"]) or "-"
    return f"{i['id']:38s} {i['categoria']:17s} {i['origem']:16s} {i['dimensoes'][0]}x{i['dimensoes'][1]:<5d} [{', '.join(i['tags'])}] uso:{uso}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(0)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "buscar":
        for i in buscar(args):
            print(_linha(i))
    elif cmd == "listar":
        for i in carregar():
            if not args or i["categoria"] == args[0]:
                print(_linha(i))
    elif cmd == "publicar":
        publicar(args[0], args[1:])
    else:
        raise SystemExit(f"comando desconhecido: {cmd}")
