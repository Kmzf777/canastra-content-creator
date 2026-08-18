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


# --- Hardening contra path traversal -----------------------------------
#
# `shortcode` chega cru do JSON do Instagram e `target_slug` chega de um
# envelope que o usuario pode ter editado a mao. Nenhum dos dois pode
# atravessar o diretorio de saida quando vira componente de caminho.


def test_nome_do_arquivo_com_shortcode_legitimo_e_identico_a_antes():
    # Prova que o sanitizador e transparente para entrada valida: o alfabeto
    # de shortcode do Instagram (A-Za-z0-9-_) passa por caminho_seguro sem
    # nenhuma alteracao.
    assert _item().filename == "2026-08-18_C1a2b3c_1.jpg"


def test_nome_do_arquivo_com_shortcode_ponto_ponto_nao_contem_ponto_ponto():
    item = _item(shortcode="..")
    assert ".." not in item.filename


@pytest.mark.parametrize("shortcode_hostil", ["../../evil", "a/b", "a\\b"])
def test_nome_do_arquivo_neutraliza_shortcode_hostil(shortcode_hostil):
    item = _item(shortcode=shortcode_hostil)
    assert "/" not in item.filename
    assert "\\" not in item.filename
    assert ".." not in item.filename


def test_nome_do_arquivo_com_shortcode_vazio_cai_para_padrao():
    item = _item(shortcode="")
    assert item.filename == "2026-08-18_sem-codigo_1.jpg"


def test_shortcode_no_modelo_continua_cru_apos_construcao():
    # Proveniencia: o sidecar registra o que o Instagram realmente disse.
    # A sanitizacao acontece so na borda (filename), nunca no campo.
    item = _item(shortcode="../../evil")
    assert item.shortcode == "../../evil"


def test_target_slug_ponto_ponto_e_neutralizado():
    lote = HarvestBatch(
        target_slug="../..",
        target_kind="profile",
        harvested_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
    )
    assert ".." not in lote.target_slug
    assert "/" not in lote.target_slug
    assert "\\" not in lote.target_slug


def test_target_slug_handle_com_ponto_fica_intacto():
    # Um handle legitimo pode ter ponto (ex.: cafe.canastra) - tem que
    # sobreviver ao saneamento sem alteracao.
    lote = HarvestBatch(
        target_slug="cafe.canastra",
        target_kind="profile",
        harvested_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
    )
    assert lote.target_slug == "cafe.canastra"


@pytest.mark.parametrize("slug_legitimo", ["post-C1a2b3c", "tag-cafeespecial"])
def test_target_slug_post_e_tag_ficam_intactos(slug_legitimo):
    lote = HarvestBatch(
        target_slug=slug_legitimo,
        target_kind="post",
        harvested_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
    )
    assert lote.target_slug == slug_legitimo


@pytest.mark.parametrize(
    "target_slug_hostil,shortcode_hostil",
    [
        ("../..", "../../evil"),
        ("../../etc/passwd", "a/b"),
        ("..\\..\\windows", "a\\b"),
    ],
)
def test_caminho_montado_com_entradas_hostis_fica_dentro_de_raspagem(
    target_slug_hostil, shortcode_hostil, tmp_path
):
    # Este e o teste que efetivamente prova a defesa: monta o caminho como o
    # codigo de producao faria e confere, via resolve(), que ele nao escapou
    # do diretorio raiz de saida.
    raiz_raspagem = tmp_path / "raspagem"
    raiz_raspagem.mkdir()

    lote = HarvestBatch(
        target_slug=target_slug_hostil,
        target_kind="profile",
        harvested_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
    )
    item = _item(shortcode=shortcode_hostil)

    caminho = (raiz_raspagem / lote.target_slug / item.filename).resolve()
    assert caminho.is_relative_to(raiz_raspagem.resolve())
