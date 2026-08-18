"""Contrato dos modelos da raspagem."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from cie.scrape.models import HarvestBatch, ScrapedItem


def _item(**over) -> ScrapedItem:
    base = dict(
        shortcode="C1a2b3c",
        owner_handle="cafecanastra",
        post_url="https://www.instagram.com/p/C1a2b3c/",
        display_url="https://scontent.cdninstagram.com/v/foto.jpg",
        width=1080,
        height=1350,
        taken_at=datetime(2026, 8, 18, 15, 30, tzinfo=timezone.utc),
        caption="colheita na fazenda",
        carousel_index=1,
        is_video=False,
    )
    base.update(over)
    return ScrapedItem(**base)


def test_item_guarda_proveniencia():
    item = _item()
    assert item.post_url.endswith("/p/C1a2b3c/")
    assert item.owner_handle == "cafecanastra"


def test_item_recusa_campo_desconhecido():
    # extra=forbid: se o Instagram mudar e alguem colar campo novo aqui,
    # o erro aparece no parser, nao tres camadas adiante.
    with pytest.raises(ValidationError):
        _item(likes=42)


def test_nome_do_arquivo_usa_data_shortcode_e_indice():
    assert _item().filename == "2026-08-18_C1a2b3c_1.jpg"


def test_nome_do_arquivo_sem_data_nao_inventa_data():
    assert _item(taken_at=None).filename == "sem-data_C1a2b3c_1.jpg"


def test_nome_do_arquivo_preserva_indice_do_carrossel():
    assert _item(carousel_index=3).filename == "2026-08-18_C1a2b3c_3.jpg"


def test_nome_do_arquivo_respeita_extensao_da_url():
    item = _item(display_url="https://scontent.cdninstagram.com/v/foto.webp?ig_cache=1")
    assert item.filename == "2026-08-18_C1a2b3c_1.webp"


def test_lote_vazio_e_valido():
    lote = HarvestBatch(
        target_slug="cafecanastra",
        target_kind="profile",
        harvested_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
    )
    assert lote.items == []
    assert lote.images == []


def test_lote_separa_imagem_de_video():
    lote = HarvestBatch(
        target_slug="cafecanastra",
        target_kind="profile",
        harvested_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
        items=[_item(), _item(shortcode="D9z", is_video=True)],
    )
    assert len(lote.items) == 2
    assert len(lote.images) == 1
    assert lote.images[0].shortcode == "C1a2b3c"
