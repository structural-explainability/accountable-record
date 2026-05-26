"""Conformance contract checks, as kit Check records.

These enforce the load-bearing conformance decisions:

- AR-D-002: applicable claims produce exactly one outcome from a *closed*
  vocabulary defined in ``data/conformance/outcomes.toml``.
- Categories such as ``warning``, ``skipped``, ``not-applicable`` and
  ``inapplicable`` are deliberately excluded from the outcome vocabulary.
- The nine accountable entity kinds (AE.*) are present, ordered 1..9, and
  carry their canonical metadata.

WHY: The outcome vocabulary is a contract surface; silently gaining or losing
an outcome is a breaking change. A check makes that change impossible by
accident. AR-specific; appended to the kit registry via registry.extend.

Converted from (root: Path) -> list[str] to the kit Check contract.
"""

from collections.abc import Iterable
from pathlib import Path
import tomllib

from se_contract_kit.resolution.context import ResolutionContext
from se_contract_kit.validation.registry import Check
from se_contract_kit.validation.results import CheckResult, cannot_verify, failure, ok

__all__ = [
    "EXPECTED_OUTCOME_IDS",
    "FORBIDDEN_OUTCOME_TOKENS",
    "EXPECTED_ENTITY_KIND_IDS",
    "OUTCOMES_CLOSED_ID",
    "NO_FORBIDDEN_OUTCOMES_ID",
    "ENTITY_KINDS_ID",
    "check_outcomes_closed",
    "check_no_forbidden_outcomes",
    "check_entity_kinds",
    "OUTCOMES_CLOSED_CHECK",
    "NO_FORBIDDEN_OUTCOMES_CHECK",
    "ENTITY_KINDS_CHECK",
    "AR_CONFORMANCE_CHECKS",
]

OUTCOMES_CLOSED_ID = "ar.conformance.outcomes-closed"
NO_FORBIDDEN_OUTCOMES_ID = "ar.conformance.no-forbidden-outcomes"
ENTITY_KINDS_ID = "ar.conformance.entity-kinds"

# REQ: The closed outcome vocabulary. Changing this set is a breaking change.
EXPECTED_OUTCOME_IDS = {"pass", "fail", "partial", "cannot-verify"}

# REQ: Outcome categories that must never appear anywhere in the contract.
FORBIDDEN_OUTCOME_TOKENS = [
    '"inapplicable"',
    '"warning"',
    '"skipped"',
    '"not-applicable"',
    '"not_applicable"',
    "Outcome.INAPPLICABLE",
]

# REQ: The nine accountable entity kinds.
EXPECTED_ENTITY_KIND_IDS = {
    "AE.OBL",
    "AE.OCC",
    "AE.REC",
    "AE.ENR_L",
    "AE.ENR_I",
    "AE.CTX_E",
    "AE.CTX_S",
    "AE.NOR_C",
    "AE.NOR_S",
}

_IGNORED_PARTS = frozenset(
    {
        ".git",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "site",
        ".ruff_cache",
        ".pytest_cache",
    }
)


def _load_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def check_outcomes_closed(context: ResolutionContext) -> Iterable[CheckResult]:
    """Outcome vocabulary must match the closed set exactly."""
    root = context.repo_root
    path = root / "data" / "conformance" / "outcomes.toml"
    if not path.is_file():
        return [
            cannot_verify(OUTCOMES_CLOSED_ID, "missing data/conformance/outcomes.toml")
        ]

    try:
        data = _load_toml(path)
    except tomllib.TOMLDecodeError as exc:
        return [
            cannot_verify(OUTCOMES_CLOSED_ID, f"invalid TOML in outcomes.toml: {exc}")
        ]

    outcomes = data.get("outcomes")
    if not isinstance(outcomes, list):
        # WHY: without [[outcomes]] rows there is nothing to evaluate the
        # vocabulary against -> cannot-verify, not a wrong-vocabulary failure.
        return [
            cannot_verify(
                OUTCOMES_CLOSED_ID, "outcomes.toml must define [[outcomes]] rows"
            )
        ]

    results: list[CheckResult] = []
    seen_ids: set[str] = set()
    required_keys = {
        "id",
        "label",
        "description",
        "is_pass",
        "is_failure",
        "evidence_sufficient",
        "blocks_mandatory_level",
    }
    for index, outcome in enumerate(outcomes, start=1):
        if not isinstance(outcome, dict):
            results.append(
                failure(OUTCOMES_CLOSED_ID, f"outcome row {index} is not a table")
            )
            continue
        missing = required_keys - set(outcome)
        if missing:
            results.append(
                failure(
                    OUTCOMES_CLOSED_ID,
                    f"outcome row {index} missing keys: {', '.join(sorted(missing))}",
                )
            )
        outcome_id = outcome.get("id")
        if isinstance(outcome_id, str):
            seen_ids.add(outcome_id)

    if seen_ids != EXPECTED_OUTCOME_IDS:
        missing_ids = sorted(EXPECTED_OUTCOME_IDS - seen_ids)
        extra_ids = sorted(seen_ids - EXPECTED_OUTCOME_IDS)
        if missing_ids:
            results.append(
                failure(
                    OUTCOMES_CLOSED_ID,
                    f"outcomes missing ids: {', '.join(missing_ids)}",
                )
            )
        if extra_ids:
            results.append(
                failure(
                    OUTCOMES_CLOSED_ID,
                    f"outcomes has unexpected ids: {', '.join(extra_ids)}",
                )
            )

    closed = data.get("closed_vocabulary")
    if not isinstance(closed, dict):
        results.append(
            failure(OUTCOMES_CLOSED_ID, "outcomes.toml must define [closed_vocabulary]")
        )
    else:
        if closed.get("only_defined_outcomes_allowed") is not True:
            results.append(
                failure(
                    OUTCOMES_CLOSED_ID,
                    "closed_vocabulary.only_defined_outcomes_allowed must be true",
                )
            )
        defined = closed.get("defined_outcomes")
        if not isinstance(defined, list) or set(defined) != EXPECTED_OUTCOME_IDS:
            results.append(
                failure(
                    OUTCOMES_CLOSED_ID,
                    "closed_vocabulary.defined_outcomes must equal the closed set",
                )
            )

    return results or [
        ok(OUTCOMES_CLOSED_ID, "outcome vocabulary is closed and complete")
    ]


def check_no_forbidden_outcomes(context: ResolutionContext) -> Iterable[CheckResult]:
    """No contract source may reference an excluded outcome category."""
    root = context.repo_root
    # WHY: skip the checks package itself, which names the forbidden tokens.
    checker_dir = Path(__file__).resolve().parent
    suffixes = {".toml", ".json", ".md"}

    results: list[CheckResult] = []
    for path in sorted((root / "data").rglob("*")):
        if path.is_dir() or path.suffix not in suffixes:
            continue
        if any(part in _IGNORED_PARTS for part in path.parts):
            continue
        if checker_dir in path.resolve().parents:
            continue
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_OUTCOME_TOKENS:
            if token in text:
                results.append(
                    failure(
                        NO_FORBIDDEN_OUTCOMES_ID,
                        f"forbidden outcome token {token!r} in {relative}",
                    )
                )

    return results or [
        ok(NO_FORBIDDEN_OUTCOMES_ID, "no forbidden outcome tokens found")
    ]


def check_entity_kinds(context: ResolutionContext) -> Iterable[CheckResult]:
    """The nine AE.* entity kinds must be present, ordered 1..9, fully described."""
    root = context.repo_root
    path = root / "data" / "entity-kinds" / "accountable_entity_kinds.toml"
    if not path.is_file():
        return [
            cannot_verify(
                ENTITY_KINDS_ID,
                "missing data/entity-kinds/accountable_entity_kinds.toml",
            )
        ]

    try:
        data = _load_toml(path)
    except tomllib.TOMLDecodeError as exc:
        return [cannot_verify(ENTITY_KINDS_ID, f"invalid TOML in {path.name}: {exc}")]

    rows = data.get("accountable_entity_kinds")
    if not isinstance(rows, list):
        return [
            cannot_verify(
                ENTITY_KINDS_ID, "must define [[accountable_entity_kinds]] rows"
            )
        ]

    results: list[CheckResult] = []
    seen_ids: set[str] = set()
    seen_orders: set[int] = set()

    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            results.append(
                failure(ENTITY_KINDS_ID, f"entity kind row {index} is not a table")
            )
            continue

        entity_id = row.get("id")
        if not isinstance(entity_id, str) or not entity_id.startswith("AE."):
            results.append(
                failure(
                    ENTITY_KINDS_ID, f"entity kind row {index} id must start with AE."
                )
            )
        else:
            seen_ids.add(entity_id)

        order = row.get("order")
        if not isinstance(order, int):
            results.append(
                failure(
                    ENTITY_KINDS_ID, f"entity kind row {index} missing integer order"
                )
            )
        else:
            seen_orders.add(order)

        for field_name in ("canonical_family", "canonical_profile", "label"):
            value = row.get(field_name)
            if not isinstance(value, str) or not value:
                results.append(
                    failure(
                        ENTITY_KINDS_ID, f"entity kind row {index} missing {field_name}"
                    )
                )

    missing_ids = sorted(EXPECTED_ENTITY_KIND_IDS - seen_ids)
    extra_ids = sorted(seen_ids - EXPECTED_ENTITY_KIND_IDS)
    if missing_ids:
        results.append(
            failure(
                ENTITY_KINDS_ID, f"entity kinds missing ids: {', '.join(missing_ids)}"
            )
        )
    if extra_ids:
        results.append(
            failure(
                ENTITY_KINDS_ID,
                f"entity kinds has unexpected ids: {', '.join(extra_ids)}",
            )
        )
    if seen_orders != set(range(1, 10)):
        results.append(
            failure(ENTITY_KINDS_ID, "entity kind orders must be exactly 1 through 9")
        )

    return results or [ok(ENTITY_KINDS_ID, "all nine entity kinds present and ordered")]


OUTCOMES_CLOSED_CHECK = Check(
    OUTCOMES_CLOSED_ID, "Outcome vocabulary is closed", check_outcomes_closed
)
NO_FORBIDDEN_OUTCOMES_CHECK = Check(
    NO_FORBIDDEN_OUTCOMES_ID, "No forbidden outcome tokens", check_no_forbidden_outcomes
)
ENTITY_KINDS_CHECK = Check(
    ENTITY_KINDS_ID, "Entity kinds present and ordered", check_entity_kinds
)

AR_CONFORMANCE_CHECKS: tuple[Check, ...] = (
    OUTCOMES_CLOSED_CHECK,
    NO_FORBIDDEN_OUTCOMES_CHECK,
    ENTITY_KINDS_CHECK,
)
