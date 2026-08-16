"""As duas UIs locais: curadoria da base real e revisao do que a IA gerou.

Tudo roda em memoria pelo TestClient - nenhuma rede, nenhuma imagem de verdade
alem dos JPEGs sinteticos da fixture.
"""

from __future__ import annotations

import itertools
import sqlite3
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from cie import capabilities, repository
from cie.capabilities import ApiCapabilities
from cie.config import Settings
from cie.enums import (
    AspectRatio,
    Location,
    Pillar,
    ReviewStatus,
    RiskFlag,
    Sku,
    TemplateKind,
)
from cie.models import Asset, Generation, Job, Template
from cie.web.app import (
    DISCLOSURE_LABEL,
    FACE_WARNING,
    PACKAGING_WARNING,
    POLICY_NOTICE,
    REJECT_REASON_REQUIRED,
    create_app,
)

#: Cabecalho que o HTMX manda; sem ele as rotas respondem com redirect 303.
HX = {"HX-Request": "true"}

_SEQUENCE = itertools.count(1)


@pytest.fixture
def client(settings: Settings, conn: sqlite3.Connection) -> TestClient:
    return TestClient(create_app(settings))


def _asset(conn: sqlite3.Connection, **overrides) -> int:
    index = next(_SEQUENCE)
    fields = {
        "path": f"/base/foto-{index:04d}.jpg",
        "sha256": f"{index:064d}",
        "width": 1600,
        "height": 1200,
        "quality_score": 80,
    }
    fields.update(overrides)
    return repository.insert_asset(conn, Asset(**fields))


def _template(
    conn: sqlite3.Connection,
    *,
    name: str = "cena-macro",
    risk_flags: tuple[RiskFlag, ...] = (),
    kind: TemplateKind = TemplateKind.MACRO,
    pillar: Pillar | None = Pillar.P3,
) -> int:
    return repository.upsert_template(
        conn,
        Template(
            name=name,
            pillar=pillar,
            kind=kind,
            body="grao de {variedade} sobre madeira crua",
            risk_flags=list(risk_flags),
        ),
    )


def _job(conn: sqlite3.Connection, template_id: int, *, refs: tuple[int, ...] = ()) -> int:
    return repository.insert_job(
        conn,
        Job(
            template_id=template_id,
            model="grok-imagine-image",
            resolved_prompt="prompt resolvido do job",
            reference_asset_ids=list(refs),
            aspect_ratio=AspectRatio.R4_3,
        ),
    )


def _generation(
    conn: sqlite3.Connection,
    job_id: int,
    *,
    path: str = "/gen/imagem.png",
    status: ReviewStatus = ReviewStatus.PENDING,
) -> int:
    index = next(_SEQUENCE)
    return repository.insert_generation(
        conn,
        Generation(
            job_id=job_id,
            path=path,
            sha256=f"{index:064d}",
            model="grok-imagine-image",
            prompt="prompt resolvido do job",
            cost_usd=0.07,
            review_status=status,
        ),
    )


def _pending(conn: sqlite3.Connection, **template_kwargs) -> int:
    """Atalho: template -> job -> generation pendente, que e o caso comum."""
    template_id = _template(conn, **template_kwargs)
    return _generation(conn, _job(conn, template_id))


# --------------------------------------------------------------------------- #
# painel
# --------------------------------------------------------------------------- #


def test_painel_avisa_que_a_api_nunca_foi_sondada(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert 'data-testid="probe-warning"' in response.text
    assert "nunca sondada" in response.text
    assert "scripts/probe_api.py" in response.text


def test_painel_troca_o_aviso_quando_a_sondagem_existe(
    client: TestClient, settings: Settings
) -> None:
    capabilities.save(settings, ApiCapabilities(probed_at="2026-08-16T12:00:00+00:00"))

    response = client.get("/")

    assert response.status_code == 200
    assert 'data-testid="probe-warning"' not in response.text
    assert 'data-testid="probe-ok"' in response.text


def test_painel_conta_assets_jobs_geracoes_e_custo(
    client: TestClient, conn: sqlite3.Connection
) -> None:
    for _ in range(7):
        _asset(conn)
    _pending(conn)

    response = client.get("/")

    assert "<b>7</b>" in response.text  # assets catalogados
    assert "US$ 0.07" in response.text  # custo acumulado da unica geracao
    assert "aguardando revisao" in response.text


# --------------------------------------------------------------------------- #
# curadoria: listagem
# --------------------------------------------------------------------------- #


def test_assets_lista_o_que_foi_inserido(client: TestClient, conn: sqlite3.Connection) -> None:
    first = _asset(conn)
    second = _asset(conn)

    response = client.get("/assets")

    assert response.status_code == 200
    assert f'id="asset-card-{first}"' in response.text
    assert f'id="asset-card-{second}"' in response.text
    # A tela precisa dizer, em voz alta, que os campos de politica sao humanos.
    assert POLICY_NOTICE in response.text


def test_assets_filtra_por_pilar(client: TestClient, conn: sqlite3.Connection) -> None:
    terroir = _asset(conn, pillar=Pillar.P1)
    laboratorio = _asset(conn, pillar=Pillar.P3)

    response = client.get("/assets", params={"pillar": Pillar.P1.value})

    assert f'id="asset-card-{terroir}"' in response.text
    assert f'id="asset-card-{laboratorio}"' not in response.text


def test_assets_filtra_por_curadoria_pendente(
    client: TestClient, conn: sqlite3.Connection
) -> None:
    pendente = _asset(conn, needs_review=True)
    pronto = _asset(conn, needs_review=False)

    response = client.get("/assets", params={"needs_review": "1"})

    assert f'id="asset-card-{pendente}"' in response.text
    assert f'id="asset-card-{pronto}"' not in response.text


def test_assets_pagina_o_grid(client: TestClient, conn: sqlite3.Connection) -> None:
    ids = [_asset(conn) for _ in range(5)]

    first_page = client.get("/assets", params={"per_page": 2, "page": 1})
    second_page = client.get("/assets", params={"per_page": 2, "page": 2})

    assert first_page.text.count('class="card asset-card"') == 2
    assert second_page.text.count('class="card asset-card"') == 2
    # A pagina 1 nao pode repetir o que a pagina 2 mostra.
    on_first = {i for i in ids if f'id="asset-card-{i}"' in first_page.text}
    on_second = {i for i in ids if f'id="asset-card-{i}"' in second_page.text}
    assert on_first and on_second and not (on_first & on_second)
    assert "proxima" in first_page.text


def test_assets_recusa_filtro_fora_do_vocabulario(client: TestClient) -> None:
    assert client.get("/assets", params={"pillar": "9"}).status_code == 400


# --------------------------------------------------------------------------- #
# curadoria: gravacao
# --------------------------------------------------------------------------- #


def test_curate_grava_politica_no_banco(client: TestClient, conn: sqlite3.Connection) -> None:
    asset_id = _asset(conn)

    response = client.post(
        f"/assets/{asset_id}/curate",
        data={
            "has_identifiable_person": "0",
            "consent_on_file": "1",
            "has_readable_packaging": "1",
            "is_reference_grade": "1",
            "needs_review": "0",
            "pillar": Pillar.P3.value,
            "sku": Sku.GEISHA.value,
            "location": Location.ESTUDIO.value,
            "notes": "conferido na curadoria",
            "notes_present": "1",
        },
        headers=HX,
    )

    assert response.status_code == 200
    assert f'id="asset-card-{asset_id}"' in response.text  # fragmento do card

    asset = repository.get_asset(conn, asset_id)
    assert asset is not None
    assert asset.has_identifiable_person is False
    assert asset.consent_on_file is True
    assert asset.has_readable_packaging is True
    assert asset.is_reference_grade is True
    assert asset.needs_review is False
    assert asset.pillar is Pillar.P3
    assert asset.sku is Sku.GEISHA
    assert asset.location is Location.ESTUDIO
    assert asset.notes == "conferido na curadoria"


def test_curate_liga_o_consentimento_e_libera_a_referencia(
    client: TestClient, conn: sqlite3.Connection
) -> None:
    # Default da ingestao: pessoa presumida presente, consentimento ausente.
    asset_id = _asset(conn, is_reference_grade=True)
    assert repository.get_asset(conn, asset_id).is_usable_as_reference is False

    client.post(f"/assets/{asset_id}/curate", data={"consent_on_file": "1"}, headers=HX)

    assert repository.get_asset(conn, asset_id).is_usable_as_reference is True


def test_curate_campo_ausente_nao_altera_nada(
    client: TestClient, conn: sqlite3.Connection
) -> None:
    asset_id = _asset(conn, consent_on_file=True, pillar=Pillar.P1)

    response = client.post(
        f"/assets/{asset_id}/curate", data={"mark_reviewed": "1"}, headers=HX
    )

    assert response.status_code == 200
    asset = repository.get_asset(conn, asset_id)
    assert asset.consent_on_file is True  # nao veio no form, nao mexe
    assert asset.pillar is Pillar.P1
    assert asset.needs_review is False  # o botao explicito vence


def test_curate_apaga_a_anotacao_quando_o_form_manda_no_campo(
    client: TestClient, conn: sqlite3.Connection
) -> None:
    asset_id = _asset(conn, notes="inferencia da ingestao: pasta sem pilar")

    # Sem `notes_present` o campo vazio nao significa nada e a nota fica.
    client.post(f"/assets/{asset_id}/curate", data={"notes": ""}, headers=HX)
    assert repository.get_asset(conn, asset_id).notes is not None

    client.post(
        f"/assets/{asset_id}/curate", data={"notes": "", "notes_present": "1"}, headers=HX
    )
    assert repository.get_asset(conn, asset_id).notes is None


def test_curate_limpa_valor_com_sentinela(
    client: TestClient, conn: sqlite3.Connection
) -> None:
    asset_id = _asset(conn, sku=Sku.CLASSICO)

    client.post(f"/assets/{asset_id}/curate", data={"sku": "__clear__"}, headers=HX)

    assert repository.get_asset(conn, asset_id).sku is None


def test_curate_sem_htmx_volta_navegando(client: TestClient, conn: sqlite3.Connection) -> None:
    asset_id = _asset(conn)

    response = client.post(
        f"/assets/{asset_id}/curate", data={"consent_on_file": "1"}, follow_redirects=False
    )

    assert response.status_code == 303
    assert repository.get_asset(conn, asset_id).consent_on_file is True


def test_curate_recusa_valor_invalido(client: TestClient, conn: sqlite3.Connection) -> None:
    asset_id = _asset(conn)

    response = client.post(
        f"/assets/{asset_id}/curate", data={"consent_on_file": "talvez"}, headers=HX
    )

    assert response.status_code == 400
    assert repository.get_asset(conn, asset_id).consent_on_file is False


def test_curate_de_asset_inexistente_da_404(client: TestClient) -> None:
    response = client.post("/assets/4242/curate", data={"consent_on_file": "1"}, headers=HX)
    assert response.status_code == 404


# --------------------------------------------------------------------------- #
# curadoria: marcacao multipla
# --------------------------------------------------------------------------- #


def test_bulk_aplica_os_mesmos_campos_a_varios(
    client: TestClient, conn: sqlite3.Connection
) -> None:
    first = _asset(conn)
    second = _asset(conn)
    untouched = _asset(conn)

    response = client.post(
        "/assets/bulk",
        data={
            "ids": [str(first), str(second)],
            "consent_on_file": "1",
            "needs_review": "0",
            "pillar": Pillar.P2.value,
        },
        headers=HX,
    )

    assert response.status_code == 200
    assert 'data-testid="bulk-result"' in response.text
    # Os cards atualizados voltam como swap fora de banda para o grid se corrigir.
    assert response.text.count('hx-swap-oob="true"') == 2

    for asset_id in (first, second):
        asset = repository.get_asset(conn, asset_id)
        assert asset.consent_on_file is True
        assert asset.needs_review is False
        assert asset.pillar is Pillar.P2

    other = repository.get_asset(conn, untouched)
    assert other.consent_on_file is False
    assert other.needs_review is True


def test_bulk_sem_selecao_ou_sem_campo_e_recusado(
    client: TestClient, conn: sqlite3.Connection
) -> None:
    asset_id = _asset(conn)

    assert client.post("/assets/bulk", data={"consent_on_file": "1"}, headers=HX).status_code == 400
    assert client.post("/assets/bulk", data={"ids": [str(asset_id)]}, headers=HX).status_code == 400


def test_bulk_ignora_id_que_nao_existe(client: TestClient, conn: sqlite3.Connection) -> None:
    asset_id = _asset(conn)

    response = client.post(
        "/assets/bulk",
        data={"ids": [str(asset_id), "9999"], "is_reference_grade": "1"},
        headers=HX,
    )

    assert response.status_code == 200
    assert "9999" in response.text
    assert repository.get_asset(conn, asset_id).is_reference_grade is True


# --------------------------------------------------------------------------- #
# arquivos servidos do disco
# --------------------------------------------------------------------------- #


def test_thumb_serve_o_arquivo_do_disco(
    client: TestClient, conn: sqlite3.Connection, settings: Settings, photo_factory
) -> None:
    thumb = photo_factory(settings.thumbs_dir / "capa.jpg", size=(320, 240))
    asset_id = _asset(conn, thumb_path=str(thumb))

    response = client.get(f"/assets/thumb/{asset_id}")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/")
    assert response.content[:2] == b"\xff\xd8"  # JPEG


def test_thumb_inexistente_da_404(
    client: TestClient, conn: sqlite3.Connection, settings: Settings
) -> None:
    sem_thumb = _asset(conn)
    apagado = _asset(conn, thumb_path=str(settings.thumbs_dir / "sumiu.jpg"))

    assert client.get(f"/assets/thumb/{sem_thumb}").status_code == 404
    assert client.get(f"/assets/thumb/{apagado}").status_code == 404
    assert client.get("/assets/thumb/4242").status_code == 404


def test_imagem_da_geracao_e_servida_e_404_quando_some(
    client: TestClient, conn: sqlite3.Connection, settings: Settings, photo_factory
) -> None:
    image = photo_factory(settings.generations_dir / "gerada.jpg", size=(640, 480))
    template_id = _template(conn)
    job_id = _job(conn, template_id)
    existente = _generation(conn, job_id, path=str(image))
    fantasma = _generation(conn, job_id, path=str(settings.generations_dir / "nao-existe.png"))

    assert client.get(f"/generations/image/{existente}").status_code == 200
    assert client.get(f"/generations/image/{fantasma}").status_code == 404
    assert client.get("/generations/image/4242").status_code == 404


# --------------------------------------------------------------------------- #
# revisao
# --------------------------------------------------------------------------- #


def test_review_mostra_so_as_pendentes(client: TestClient, conn: sqlite3.Connection) -> None:
    template_id = _template(conn)
    job_id = _job(conn, template_id)
    pendente = _generation(conn, job_id)
    aprovada = _generation(conn, job_id, status=ReviewStatus.APPROVED)
    rejeitada = _generation(conn, job_id, status=ReviewStatus.REJECTED)

    response = client.get("/review")

    assert response.status_code == 200
    assert f'id="gen-card-{pendente}"' in response.text
    assert f'id="gen-card-{aprovada}"' not in response.text
    assert f'id="gen-card-{rejeitada}"' not in response.text


def test_review_mostra_proveniencia_e_selo_de_disclosure(
    client: TestClient, conn: sqlite3.Connection
) -> None:
    reference = _asset(conn, is_reference_grade=True, consent_on_file=True)
    template_id = _template(conn, name="macro-terreiro")
    job_id = _job(conn, template_id, refs=(reference,))
    generation_id = _generation(conn, job_id)

    response = client.get("/review")

    assert "macro-terreiro" in response.text
    assert "prompt resolvido do job" in response.text
    assert f'src="/assets/thumb/{reference}"' in response.text
    assert DISCLOSURE_LABEL in response.text
    assert f'data-id="{generation_id}"' in response.text


def test_review_avisa_sobre_tipografia_quando_o_template_toca_embalagem(
    client: TestClient, conn: sqlite3.Connection
) -> None:
    _pending(conn, name="packshot-classico", risk_flags=(RiskFlag.PACKAGING_TEXT,))

    response = client.get("/review")

    assert 'data-testid="packaging-warning"' in response.text
    assert PACKAGING_WARNING in response.text


def test_review_nao_avisa_sobre_tipografia_em_cena_sem_embalagem(
    client: TestClient, conn: sqlite3.Connection
) -> None:
    _pending(conn, name="macro-sem-rotulo")

    response = client.get("/review")

    assert 'data-testid="packaging-warning"' not in response.text
    assert PACKAGING_WARNING not in response.text


def test_review_avisa_sobre_rosto_humano(client: TestClient, conn: sqlite3.Connection) -> None:
    _pending(conn, name="retrato-torra", risk_flags=(RiskFlag.HUMAN_FACE,))

    response = client.get("/review")

    assert FACE_WARNING in response.text


def test_approve_muda_o_status(client: TestClient, conn: sqlite3.Connection) -> None:
    generation_id = _pending(conn)

    response = client.post(f"/generations/{generation_id}/approve", headers=HX)

    assert response.status_code == 200
    assert "aprovada" in response.text
    generation = repository.get_generation(conn, generation_id)
    assert generation.review_status is ReviewStatus.APPROVED
    assert generation.reject_reason is None


def test_reject_grava_o_motivo(client: TestClient, conn: sqlite3.Connection) -> None:
    generation_id = _pending(conn)

    response = client.post(
        f"/generations/{generation_id}/reject",
        data={"reject_reason": "tipografia do rotulo saiu deformada"},
        headers=HX,
    )

    assert response.status_code == 200
    generation = repository.get_generation(conn, generation_id)
    assert generation.review_status is ReviewStatus.REJECTED
    assert generation.reject_reason == "tipografia do rotulo saiu deformada"
    assert "tipografia do rotulo saiu deformada" in response.text


def test_reject_sem_motivo_e_recusado(client: TestClient, conn: sqlite3.Connection) -> None:
    generation_id = _pending(conn)

    response = client.post(
        f"/generations/{generation_id}/reject", data={"reject_reason": "   "}, headers=HX
    )

    assert response.status_code == 400
    assert REJECT_REASON_REQUIRED in response.json()["detail"]
    assert repository.get_generation(conn, generation_id).review_status is ReviewStatus.PENDING


def test_decisao_sem_htmx_volta_navegando(client: TestClient, conn: sqlite3.Connection) -> None:
    generation_id = _pending(conn)

    response = client.post(f"/generations/{generation_id}/approve", follow_redirects=False)

    assert response.status_code == 303
    assert repository.get_generation(conn, generation_id).review_status is ReviewStatus.APPROVED


def test_decisao_sobre_geracao_inexistente_da_404(client: TestClient) -> None:
    assert client.post("/generations/4242/approve", headers=HX).status_code == 404
    assert (
        client.post("/generations/4242/reject", data={"reject_reason": "x"}, headers=HX).status_code
        == 404
    )


# --------------------------------------------------------------------------- #
# ponto focal
# --------------------------------------------------------------------------- #


def test_focal_grava_ponto_relativo(client: TestClient, conn: sqlite3.Connection) -> None:
    generation_id = _pending(conn)

    response = client.post(
        f"/generations/{generation_id}/focal", data={"x": "0.25", "y": "0.75"}
    )

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert repository.get_focal_point(conn, generation_id) == (0.25, 0.75)


@pytest.mark.parametrize("point", [{"x": "1.5", "y": "0.5"}, {"x": "0.5", "y": "-0.1"}])
def test_focal_recusa_valor_fora_de_zero_um(
    client: TestClient, conn: sqlite3.Connection, point: dict[str, str]
) -> None:
    generation_id = _pending(conn)

    response = client.post(f"/generations/{generation_id}/focal", data=point)

    assert response.status_code == 400
    assert repository.get_focal_point(conn, generation_id) is None


def test_focal_aparece_na_tela_de_revisao(client: TestClient, conn: sqlite3.Connection) -> None:
    generation_id = _pending(conn)
    client.post(f"/generations/{generation_id}/focal", data={"x": "0.4", "y": "0.6"})

    response = client.get("/review")

    assert "focal-dot" in response.text
    assert "left: 40.0%" in response.text


def test_focal_de_geracao_inexistente_da_404(client: TestClient) -> None:
    response = client.post("/generations/4242/focal", data={"x": "0.5", "y": "0.5"})
    assert response.status_code == 404
