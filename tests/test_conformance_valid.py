"""Tests for conformance source data."""

from pathlib import Path
import tomllib


def repo_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[1]


def load_toml(relative_path: str) -> dict[str, object]:
    """Load a TOML file from the repository root."""
    path = repo_root() / relative_path
    with path.open("rb") as file:
        return tomllib.load(file)


def test_conformance_outcomes_are_closed_and_complete() -> None:
    """Conformance outcomes define the closed AR outcome vocabulary."""
    data = load_toml("data/conformance/outcomes.toml")

    outcomes = data.get("outcomes")
    assert isinstance(outcomes, list)

    outcome_ids = [outcome["id"] for outcome in outcomes if isinstance(outcome, dict)]

    expected_ids = {
        "cannot-verify",
        "fail",
        "partial",
        "pass",
    }

    assert set(outcome_ids) == expected_ids
    assert len(outcome_ids) == len(set(outcome_ids))

    closed_vocabulary = data.get("closed_vocabulary")
    assert isinstance(closed_vocabulary, dict)
    assert closed_vocabulary["only_defined_outcomes_allowed"] is True
    assert set(closed_vocabulary["defined_outcomes"]) == expected_ids


def test_conformance_outcomes_have_required_flags() -> None:
    """Each outcome declares pass/failure/evidence/level semantics."""
    data = load_toml("data/conformance/outcomes.toml")

    outcomes = data.get("outcomes")
    assert isinstance(outcomes, list)

    required_keys = {
        "id",
        "label",
        "description",
        "is_pass",
        "is_failure",
        "evidence_sufficient",
        "blocks_mandatory_level",
    }

    for outcome in outcomes:
        assert isinstance(outcome, dict)
        assert required_keys <= set(outcome)


def test_cannot_verify_marks_evidence_insufficient() -> None:
    """cannot-verify means required evidence is missing."""
    data = load_toml("data/conformance/outcomes.toml")

    outcomes = data.get("outcomes")
    assert isinstance(outcomes, list)

    by_id = {
        outcome["id"]: outcome for outcome in outcomes if isinstance(outcome, dict)
    }

    assert by_id["cannot-verify"]["evidence_sufficient"] is False
    assert by_id["fail"]["evidence_sufficient"] is True
    assert by_id["partial"]["evidence_sufficient"] is True
    assert by_id["pass"]["evidence_sufficient"] is True


def test_composite_claim_rollup_is_failure_first() -> None:
    """Composite claims preserve known failures over missing evidence."""
    data = load_toml("data/conformance/outcomes.toml")

    rollup = data.get("composite_claim_rollup")
    assert isinstance(rollup, dict)

    rules = rollup.get("rules")
    assert isinstance(rules, dict)

    assert rules["any_required_requirement_fail_makes_claim_fail"] is True
    assert (
        rules[
            "otherwise_any_required_requirement_cannot_verify_makes_claim_cannot_verify"
        ]
        is True
    )
    assert rollup["unknown_requirement_outcome_is_an_error"] is True

    precedence = rollup.get("precedence")
    assert isinstance(precedence, dict)
    assert precedence == {
        "first": "fail",
        "second": "partial",
        "third": "cannot-verify",
        "fourth": "pass",
    }


def test_report_semantics_distinguish_evidence_from_missing_evidence() -> None:
    """Report semantics do not require missing evidence to be present."""
    data = load_toml("data/conformance/report-semantics.toml")

    evidence = data.get("evidence")
    assert isinstance(evidence, dict)

    assert evidence["required_for_outcomes"] == [
        "fail",
        "partial",
    ]
    assert evidence["missing_evidence_must_be_identified_for_outcomes"] == [
        "cannot-verify",
    ]
