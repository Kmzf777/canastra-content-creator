"""Download, dedupe e sidecar. httpx nunca e chamado de verdade aqui."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from cie.scrape.download import DownloadReport, download_batch
from cie.scrape.models import HarvestBatch, ScrapedItem


def _item(shortcode="AAA111", indice=1, url=None, is_video=False) -> ScrapedItem:
    return ScrapedItem(
        shortcode=shortcode,
        owner_handle="cafecanastra",
        post_url=f"https://www.instagram.com/p/{shortcode}/",
        display_url=url or f"https://cdn.example/{shortcode}-{indice}.jpg",
        width=1080,
        height=1350,
        taken_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
        caption="legenda",
        carousel_index=indice,
        is_video=is_video,
    )


def _lote(*itens) -> HarvestBatch:
    return HarvestBatch(
        target_slug="cafecanastra",
        target_kind="profile",
        harvested_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
        items=list(itens),
    )


def _buscador(mapa: dict[str, bytes]):
    """Substitui httpx: URL -> bytes. Registra o que foi pedido."""
    pedidos: list[str] = []

    def buscar(url: str) -> bytes:
        pedidos.append(url)
        if url not in mapa:
            raise RuntimeError(f"404 {url}")
        return mapa[url]

    buscar.pedidos = pedidos
    return buscar


def test_baixa_e_grava_arquivo_com_nome_previsivel(tmp_path: Path):
    item = _item()
    buscar = _buscador({item.display_url: b"conteudo-da-foto"})

    relatorio = download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    destino = tmp_path / "cafecanastra" / "2026-08-18_AAA111_1.jpg"
    assert destino.is_file()
    assert destino.read_bytes() == b"conteudo-da-foto"
    assert relatorio.baixados == 1


def test_sidecar_guarda_proveniencia_completa(tmp_path: Path):
    item = _item()
    buscar = _buscador({item.display_url: b"conteudo-da-foto"})

    download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    sidecar = tmp_path / "cafecanastra" / "2026-08-18_AAA111_1.json"
    dados = json.loads(sidecar.read_text(encoding="utf-8"))
    assert dados["post_url"] == "https://www.instagram.com/p/AAA111/"
    assert dados["owner_handle"] == "cafecanastra"
    assert dados["shortcode"] == "AAA111"
    assert dados["carousel_index"] == 1
    assert dados["source_url"] == item.display_url
    assert dados["width"] == 1080
    assert len(dados["sha256"]) == 64
    assert dados["scraped_at"]
    # A raspagem nao opina sobre pessoa nem consentimento - isso e da curadoria.
    assert "has_identifiable_person" not in dados
    assert "consent_on_file" not in dados


def test_video_nunca_e_baixado(tmp_path: Path):
    item = _item(is_video=True)
    buscar = _buscador({item.display_url: b"capa-de-video"})

    relatorio = download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    assert buscar.pedidos == []
    assert relatorio.baixados == 0
    assert relatorio.videos_pulados == 1


def test_conteudo_repetido_e_pulado_por_sha256(tmp_path: Path):
    # Dois shortcodes diferentes, mesmo byte a byte: so um arquivo sobrevive.
    a = _item(shortcode="AAA111")
    b = _item(shortcode="BBB222")
    buscar = _buscador({a.display_url: b"identico", b.display_url: b"identico"})

    relatorio = download_batch(_lote(a, b), out_root=tmp_path, fetch=buscar, delay=0)

    assert relatorio.baixados == 1
    assert relatorio.duplicados == 1
    assert len(list((tmp_path / "cafecanastra").glob("*.jpg"))) == 1


def test_dedupe_atravessa_execucoes(tmp_path: Path):
    item = _item()
    buscar = _buscador({item.display_url: b"identico"})

    download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)
    segundo = download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    assert segundo.baixados == 0
    assert segundo.duplicados == 1


def test_nada_sobrescreve_arquivo_existente(tmp_path: Path):
    destino = tmp_path / "cafecanastra" / "2026-08-18_AAA111_1.jpg"
    destino.parent.mkdir(parents=True)
    destino.write_bytes(b"ja-estava-aqui")

    item = _item()
    buscar = _buscador({item.display_url: b"conteudo-novo"})
    relatorio = download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    assert destino.read_bytes() == b"ja-estava-aqui"
    assert relatorio.baixados == 1
    # o novo entrou com sufixo, sem destruir o que existia
    assert (tmp_path / "cafecanastra" / "2026-08-18_AAA111_1-2.jpg").is_file()


def test_dry_run_nao_escreve_nada(tmp_path: Path):
    item = _item()
    buscar = _buscador({item.display_url: b"conteudo"})

    relatorio = download_batch(
        _lote(item), out_root=tmp_path, fetch=buscar, delay=0, dry_run=True
    )

    assert buscar.pedidos == []
    assert list(tmp_path.rglob("*.jpg")) == []
    assert relatorio.dry_run is True
    assert relatorio.previstos == 1


def test_falha_de_rede_nao_derruba_o_lote(tmp_path: Path):
    bom = _item(shortcode="AAA111")
    ruim = _item(shortcode="BBB222")
    buscar = _buscador({bom.display_url: b"ok"})  # o de BBB222 vai levantar

    relatorio = download_batch(_lote(bom, ruim), out_root=tmp_path, fetch=buscar, delay=0)

    assert relatorio.baixados == 1
    assert relatorio.erros == 1
    assert "BBB222" in relatorio.mensagens_de_erro()[0]


def test_limit_corta_o_lote(tmp_path: Path):
    itens = [_item(shortcode=f"S{i}") for i in range(5)]
    buscar = _buscador({i.display_url: f"foto-{i.shortcode}".encode() for i in itens})

    relatorio = download_batch(_lote(*itens), out_root=tmp_path, fetch=buscar, delay=0, limit=2)

    assert relatorio.baixados == 2


def test_manifest_do_lote_e_gravado(tmp_path: Path):
    item = _item()
    buscar = _buscador({item.display_url: b"conteudo"})

    download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    manifest = json.loads((tmp_path / "_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["arquivos"]) == 1
    registro = manifest["arquivos"][0]
    assert registro["path"] == "cafecanastra/2026-08-18_AAA111_1.jpg"
    assert len(registro["sha256"]) == 64


def test_manifest_acumula_entre_execucoes(tmp_path: Path):
    a = _item(shortcode="AAA111")
    b = _item(shortcode="BBB222")
    download_batch(_lote(a), out_root=tmp_path, fetch=_buscador({a.display_url: b"a"}), delay=0)
    download_batch(_lote(b), out_root=tmp_path, fetch=_buscador({b.display_url: b"b"}), delay=0)

    manifest = json.loads((tmp_path / "_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["arquivos"]) == 2


def test_relatorio_vazio_e_valido(tmp_path: Path):
    relatorio = download_batch(_lote(), out_root=tmp_path, fetch=_buscador({}), delay=0)
    assert isinstance(relatorio, DownloadReport)
    assert relatorio.baixados == 0
