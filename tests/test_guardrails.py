"""Um teste por regra, mais os casos de borda que a politica nao pode errar."""

from __future__ import annotations

import pytest

from cie import guardrails, pricing
from cie.capabilities import ApiCapabilities
from cie.enums import AspectRatio, Pillar, RiskFlag, TemplateKind
from cie.errors import GuardrailViolation
from cie.guardrails import GuardrailContext, Severity
from cie.models import Asset, Template
from cie.pricing import ImageModel


def make_template(**overrides) -> Template:
    base = dict(
        name="p3_tambor_macro",
        pillar=Pillar.P3,
        kind=TemplateKind.MACRO,
        body="macro do tambor de torra, luz lateral quente, textura de metal escovado",
        requires_reference=False,
        risk_flags=[],
        default_aspect_ratio=AspectRatio.R1_1,
    )
    base.update(overrides)
    return Template(**base)


def make_asset(**overrides) -> Asset:
    """Asset default: referencia limpa, sem pessoa, sem embalagem legivel."""
    base = dict(
        id=1,
        path="/base/CANASTRA_3_TORREFACAO_TAMBOR_001.jpg",
        sha256="a" * 64,
        width=4000,
        height=3000,
        has_identifiable_person=False,
        consent_on_file=False,
        has_readable_packaging=False,
        quality_score=82,
        is_reference_grade=True,
    )
    base.update(overrides)
    return Asset(**base)


def rules_by_name(report) -> dict[str, guardrails.GuardrailResult]:
    return {r.rule: r for r in report.results}


def blocking_rules(report) -> list[str]:
    return [r.rule for r in report.blocking]


def warning_rules(report) -> list[str]:
    return [r.rule for r in report.warnings]


# --------------------------------------------------------------------------- #
# base
# --------------------------------------------------------------------------- #


def test_clean_context_is_not_blocked():
    report = guardrails.evaluate(GuardrailContext(template=make_template()))

    assert report.blocked is False
    assert report.blocking == []
    assert report.disclosure_required is True


def test_empty_asset_list_passes_every_asset_rule():
    """Lista vazia nao pode virar bloqueio acidental nas regras de asset."""
    report = guardrails.evaluate(GuardrailContext(template=make_template(), assets=[]))
    results = rules_by_name(report)

    assert results["no_synthetic_identifiable_faces"].passed is True
    assert results["reference_quality"].passed is True
    assert results["max_reference_images"].passed is True
    assert "native_reference_capability" not in results


# --------------------------------------------------------------------------- #
# 1. no_synthetic_identifiable_faces
# --------------------------------------------------------------------------- #


def test_person_without_consent_is_blocked():
    asset = make_asset(has_identifiable_person=True, consent_on_file=False)
    report = guardrails.evaluate(GuardrailContext(template=make_template(), assets=[asset]))

    assert report.blocked is True
    assert "no_synthetic_identifiable_faces" in blocking_rules(report)
    violation = rules_by_name(report)["no_synthetic_identifiable_faces"]
    assert violation.severity is Severity.BLOCK
    assert "consent" in violation.remedy


def test_person_with_consent_passes():
    asset = make_asset(has_identifiable_person=True, consent_on_file=True)
    report = guardrails.evaluate(GuardrailContext(template=make_template(), assets=[asset]))

    assert report.blocked is False
    assert rules_by_name(report)["no_synthetic_identifiable_faces"].passed is True


# --------------------------------------------------------------------------- #
# 2. face_regeneration_forbidden
# --------------------------------------------------------------------------- #


def test_face_regeneration_blocks_even_with_signed_consent():
    """Borda critica: passa na regra 1 (tem consentimento) e cai na 2 mesmo assim."""
    asset = make_asset(has_identifiable_person=True, consent_on_file=True)
    template = make_template(risk_flags=[RiskFlag.FACE_REGENERATION])

    report = guardrails.evaluate(GuardrailContext(template=template, assets=[asset]))
    results = rules_by_name(report)

    assert results["no_synthetic_identifiable_faces"].passed is True
    assert results["face_regeneration_forbidden"].passed is False
    assert blocking_rules(report) == ["face_regeneration_forbidden"]


def test_face_regeneration_template_without_people_is_allowed():
    template = make_template(risk_flags=[RiskFlag.FACE_REGENERATION])
    report = guardrails.evaluate(
        GuardrailContext(template=template, assets=[make_asset(has_identifiable_person=False)])
    )

    assert report.blocked is False
    assert rules_by_name(report)["face_regeneration_forbidden"].passed is True


# --------------------------------------------------------------------------- #
# 3. packaging_requires_reference
# --------------------------------------------------------------------------- #


def test_requires_reference_without_assets_is_blocked():
    template = make_template(requires_reference=True)
    report = guardrails.evaluate(GuardrailContext(template=template))

    assert blocking_rules(report) == ["packaging_requires_reference"]


def test_requires_reference_with_asset_passes():
    template = make_template(requires_reference=True)
    report = guardrails.evaluate(
        GuardrailContext(template=template, assets=[make_asset()])
    )

    assert report.blocked is False


def test_packaging_template_needs_asset_with_readable_packaging():
    template = make_template(
        kind=TemplateKind.PRODUCT_SHOT,
        pillar=Pillar.PRODUCT,
        risk_flags=[RiskFlag.PACKAGING_TEXT],
    )
    without = guardrails.evaluate(
        GuardrailContext(template=template, assets=[make_asset(has_readable_packaging=False)])
    )
    with_packaging = guardrails.evaluate(
        GuardrailContext(template=template, assets=[make_asset(has_readable_packaging=True)])
    )

    assert "packaging_requires_reference" in blocking_rules(without)
    assert with_packaging.blocked is False


def test_compositor_flips_the_verdict_and_emits_info():
    template = make_template(
        kind=TemplateKind.PRODUCT_SHOT,
        risk_flags=[RiskFlag.PACKAGING_TEXT],
    )
    blocked = guardrails.evaluate(GuardrailContext(template=template))
    composed = guardrails.evaluate(
        GuardrailContext(template=template, use_compositor=True, has_cutout_available=True)
    )

    assert blocked.blocked is True
    assert composed.blocked is False
    infos = [r for r in composed.infos if r.rule == "packaging_requires_reference"]
    assert infos and "composicao local" in infos[0].message


def test_compositor_info_flags_missing_cutout():
    template = make_template(requires_reference=True)
    report = guardrails.evaluate(
        GuardrailContext(template=template, use_compositor=True, has_cutout_available=False)
    )

    infos = [r for r in report.infos if r.rule == "packaging_requires_reference"]
    assert report.blocked is False
    assert infos and "nenhum recorte" in infos[0].message


# --------------------------------------------------------------------------- #
# 4. packaging_typography_review
# --------------------------------------------------------------------------- #


def test_packaging_text_always_warns_about_typography():
    template = make_template(risk_flags=[RiskFlag.PACKAGING_TEXT])
    report = guardrails.evaluate(
        GuardrailContext(template=template, assets=[make_asset(has_readable_packaging=True)])
    )

    assert report.blocked is False
    assert "packaging_typography_review" in warning_rules(report)
    assert report.typography_review_required is True


def test_template_without_packaging_has_no_typography_warning():
    report = guardrails.evaluate(GuardrailContext(template=make_template()))

    assert report.typography_review_required is False
    assert "packaging_typography_review" not in warning_rules(report)


# --------------------------------------------------------------------------- #
# 5. reference_quality
# --------------------------------------------------------------------------- #


def test_non_reference_grade_asset_is_blocked():
    report = guardrails.evaluate(
        GuardrailContext(
            template=make_template(),
            assets=[make_asset(id=9, is_reference_grade=False)],
        )
    )

    assert "reference_quality" in blocking_rules(report)
    assert "#9" in rules_by_name(report)["reference_quality"].message


# --------------------------------------------------------------------------- #
# 6. max_reference_images
# --------------------------------------------------------------------------- #


def test_three_references_pass_and_four_block():
    three = [make_asset(id=i) for i in range(1, 4)]
    four = [make_asset(id=i) for i in range(1, 5)]

    ok = guardrails.evaluate(GuardrailContext(template=make_template(), assets=three))
    too_many = guardrails.evaluate(GuardrailContext(template=make_template(), assets=four))

    assert ok.blocked is False
    assert blocking_rules(too_many) == ["max_reference_images"]


# --------------------------------------------------------------------------- #
# 7 e 8. riscos de maos e rosto
# --------------------------------------------------------------------------- #


def test_hands_flag_warns_without_blocking():
    template = make_template(risk_flags=[RiskFlag.HANDS])
    report = guardrails.evaluate(GuardrailContext(template=template))

    assert report.blocked is False
    assert "hands_risk" in warning_rules(report)


def test_human_face_flag_warns_without_blocking():
    template = make_template(pillar=Pillar.PEOPLE, risk_flags=[RiskFlag.HUMAN_FACE])
    report = guardrails.evaluate(GuardrailContext(template=template))

    assert report.blocked is False
    assert "human_face_risk" in warning_rules(report)


# --------------------------------------------------------------------------- #
# 9 e 10. limites do modelo
# --------------------------------------------------------------------------- #


@pytest.fixture
def narrow_model(monkeypatch: pytest.MonkeyPatch) -> ImageModel:
    """Modelo de teste com uma unica proporcao e tiragem curta."""
    model = ImageModel(
        name="modelo-estreito",
        prices_usd={"1k": 0.03},
        max_n=2,
        aspect_ratios=("1:1",),
    )
    monkeypatch.setitem(pricing.CATALOG, model.name, model)
    return model


def test_unsupported_aspect_ratio_is_blocked(narrow_model):
    report = guardrails.evaluate(
        GuardrailContext(
            template=make_template(),
            model=narrow_model.name,
            aspect_ratio=AspectRatio.R9_16,
        )
    )

    assert "aspect_ratio_supported" in blocking_rules(report)
    assert "9:16" in rules_by_name(report)["aspect_ratio_supported"].message


def test_supported_aspect_ratio_passes(narrow_model):
    report = guardrails.evaluate(
        GuardrailContext(
            template=make_template(),
            model=narrow_model.name,
            aspect_ratio=AspectRatio.R1_1,
        )
    )

    assert "aspect_ratio_supported" not in blocking_rules(report)


@pytest.mark.parametrize("n", [0, -1, 11, 50])
def test_n_outside_limits_is_blocked(n: int):
    report = guardrails.evaluate(GuardrailContext(template=make_template(), n=n))

    assert "n_within_limits" in blocking_rules(report)


@pytest.mark.parametrize("n", [1, 5, 10])
def test_n_inside_limits_passes(n: int):
    report = guardrails.evaluate(GuardrailContext(template=make_template(), n=n))

    assert report.blocked is False


def test_model_max_n_is_respected(narrow_model):
    report = guardrails.evaluate(
        GuardrailContext(template=make_template(), model=narrow_model.name, n=3)
    )

    assert "n_within_limits" in blocking_rules(report)
    assert "1..2" in rules_by_name(report)["n_within_limits"].message


# --------------------------------------------------------------------------- #
# 11. prompt_body_present
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("body", ["", "   ", "\n\t"])
def test_empty_template_body_is_blocked(body: str):
    report = guardrails.evaluate(GuardrailContext(template=make_template(body=body)))

    assert "prompt_body_present" in blocking_rules(report)


# --------------------------------------------------------------------------- #
# 12. native_reference_capability
# --------------------------------------------------------------------------- #


def test_reference_without_probe_warns_but_never_blocks():
    report = guardrails.evaluate(
        GuardrailContext(template=make_template(), assets=[make_asset()], capabilities=None)
    )

    assert report.blocked is False
    warning = rules_by_name(report)["native_reference_capability"]
    assert warning.severity is Severity.WARN
    assert "probe_api.py" in warning.remedy


def test_unprobed_capabilities_object_also_warns():
    report = guardrails.evaluate(
        GuardrailContext(
            template=make_template(),
            assets=[make_asset()],
            capabilities=ApiCapabilities(),
        )
    )

    assert "native_reference_capability" in warning_rules(report)


def test_probed_native_reference_removes_the_warning():
    caps = ApiCapabilities(
        probed_at="2026-01-01T00:00:00Z",
        native_reference_supported=True,
        reference_field="image",
        reference_endpoint="/images/edits",
        max_reference_images=2,
    )
    report = guardrails.evaluate(
        GuardrailContext(template=make_template(), assets=[make_asset()], capabilities=caps)
    )

    assert "native_reference_capability" not in warning_rules(report)


# --------------------------------------------------------------------------- #
# 13. compositor_preferred_for_product_shot
# --------------------------------------------------------------------------- #


def test_product_shot_with_cutout_prefers_the_compositor():
    template = make_template(kind=TemplateKind.PRODUCT_SHOT, requires_reference=False)
    report = guardrails.evaluate(
        GuardrailContext(template=template, has_cutout_available=True, use_compositor=False)
    )

    assert "compositor_preferred_for_product_shot" in warning_rules(report)


def test_no_compositor_hint_when_already_composing_or_without_cutout():
    template = make_template(kind=TemplateKind.PRODUCT_SHOT)
    composing = guardrails.evaluate(
        GuardrailContext(template=template, has_cutout_available=True, use_compositor=True)
    )
    no_cutout = guardrails.evaluate(
        GuardrailContext(template=template, has_cutout_available=False)
    )

    assert "compositor_preferred_for_product_shot" not in warning_rules(composing)
    assert "compositor_preferred_for_product_shot" not in warning_rules(no_cutout)


# --------------------------------------------------------------------------- #
# 14 e 15. disclosure e catalogo
# --------------------------------------------------------------------------- #


def test_disclosure_is_always_reported_as_info():
    report = guardrails.evaluate(GuardrailContext(template=make_template()))
    disclosure = rules_by_name(report)["disclosure_required"]

    assert disclosure.severity is Severity.INFO
    assert disclosure.passed is True
    assert report.disclosure_required is True


def test_unverified_model_warns():
    report = guardrails.evaluate(
        GuardrailContext(template=make_template(), model=pricing.DEFAULT_MODEL)
    )

    assert "model_not_verified" in warning_rules(report)


def test_verified_model_does_not_warn(monkeypatch: pytest.MonkeyPatch):
    model = ImageModel(
        name="modelo-sondado",
        prices_usd={"1k": 0.02},
        verified=True,
        source="sondagem da API",
    )
    monkeypatch.setitem(pricing.CATALOG, model.name, model)

    report = guardrails.evaluate(GuardrailContext(template=make_template(), model=model.name))

    assert "model_not_verified" not in warning_rules(report)


def test_unknown_model_never_raises():
    report = guardrails.evaluate(
        GuardrailContext(template=make_template(), model="modelo-que-nao-existe")
    )

    assert "model_not_verified" in warning_rules(report)
    assert report.blocked is False


# --------------------------------------------------------------------------- #
# relatorio e enforce
# --------------------------------------------------------------------------- #


def test_enforce_raises_with_rule_name_and_remedy():
    asset = make_asset(id=7, has_identifiable_person=True, consent_on_file=False)
    ctx = GuardrailContext(template=make_template(), assets=[asset])

    with pytest.raises(GuardrailViolation) as excinfo:
        guardrails.enforce(ctx)

    exc = excinfo.value
    assert exc.rule == "no_synthetic_identifiable_faces"
    assert "[no_synthetic_identifiable_faces]" in str(exc)
    assert exc.remedy and exc.remedy in str(exc)
    assert "como resolver" in str(exc)


def test_enforce_returns_the_report_when_nothing_blocks():
    report = guardrails.enforce(GuardrailContext(template=make_template()))

    assert report.blocked is False
    assert report.results


def test_raise_if_blocked_reports_the_person_rule_first():
    """Varios bloqueios ao mesmo tempo: a politica de pessoas vem antes do resto."""
    asset = make_asset(has_identifiable_person=True, is_reference_grade=False)
    ctx = GuardrailContext(
        template=make_template(body="", requires_reference=True), assets=[asset], n=0
    )
    report = guardrails.evaluate(ctx)

    assert len(report.blocking) > 1
    with pytest.raises(GuardrailViolation) as excinfo:
        report.raise_if_blocked()
    assert excinfo.value.rule == "no_synthetic_identifiable_faces"


def test_as_rows_is_printable():
    report = guardrails.evaluate(
        GuardrailContext(
            template=make_template(risk_flags=[RiskFlag.HANDS]), assets=[make_asset()]
        )
    )
    rows = report.as_rows()

    assert len(rows) == len(report.results)
    assert set(rows[0]) == {"regra", "severidade", "ok", "mensagem", "como_resolver"}
    assert {"block", "warn", "info"} >= {row["severidade"] for row in rows}
    assert all(isinstance(row["severidade"], str) for row in rows)


def test_every_rule_returns_the_declared_shape():
    """Contrato de RULES: GuardrailResult, lista deles, ou None."""
    ctx = GuardrailContext(template=make_template(), assets=[make_asset()])

    for rule in guardrails.RULES:
        outcome = rule(ctx)
        assert outcome is None or isinstance(
            outcome, (guardrails.GuardrailResult, list)
        )
        if isinstance(outcome, list):
            assert all(isinstance(item, guardrails.GuardrailResult) for item in outcome)
