"""Conformance contract checks.

These enforce the load-bearing conformance decisions:

- AR-D-002: applicable claims produce exactly one outcome from a *closed*
  vocabulary defined in ``data/conformance/outcomes.toml``.
- Categories such as ``warning``, ``skipped``, ``not-applicable`` and
  ``inapplicable`` are deliberately excluded from the outcome vocabulary.
- The nine accountable entity kinds (AE.*) are present, ordered 1..9, and
  carry their canonical metadata.

WHY: The outcome vocabulary is a contract surface; silently gaining or losing
an outcome is a breaking change. A check makes that change impossible to make
by accident.
"""

from pathlib import Path
import tomllib

# REQ: The closed outcome vocabulary. Changing this set is a breaking change.
EXPECTED_OUTCOME_IDS = {
    "pass",
    "fail",
    "partial",
    "cannot-verify",
}

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


def _load_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def check_outcomes_closed(root: Path) -> list[str]:
    """Outcome vocabulary must match the closed set exactly."""
    path = root / "data" / "conformance" / "outcomes.toml"
    if not path.is_file():
        return ["missing data/conformance/outcomes.toml"]

    try:
        data = _load_toml(path)
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid TOML in data/conformance/outcomes.toml: {exc}"]

    failures: list[str] = []

    outcomes = data.get("outcomes")
    if not isinstance(outcomes, list):
        return ["outcomes.toml must define [[outcomes]] rows"]

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
            failures.append(f"outcome row {index} is not a table")
            continue
        missing = required_keys - set(outcome)
        if missing:
            failures.append(
                f"outcome row {index} missing keys: {', '.join(sorted(missing))}"
            )
        outcome_id = outcome.get("id")
        if isinstance(outcome_id, str):
            seen_ids.add(outcome_id)

    if seen_ids != EXPECTED_OUTCOME_IDS:
        missing_ids = sorted(EXPECTED_OUTCOME_IDS - seen_ids)
        extra_ids = sorted(seen_ids - EXPECTED_OUTCOME_IDS)
        if missing_ids:
            failures.append(f"outcomes missing ids: {', '.join(missing_ids)}")
        if extra_ids:
            failures.append(f"outcomes has unexpected ids: {', '.join(extra_ids)}")

    closed = data.get("closed_vocabulary")
    if not isinstance(closed, dict):
        failures.append("outcomes.toml must define [closed_vocabulary]")
    else:
        if closed.get("only_defined_outcomes_allowed") is not True:
            failures.append(
                "closed_vocabulary.only_defined_outcomes_allowed must be true"
            )
        defined = closed.get("defined_outcomes")
        if not isinstance(defined, list) or set(defined) != EXPECTED_OUTCOME_IDS:
            failures.append(
                "closed_vocabulary.defined_outcomes must equal the closed set"
            )

    return failures


def check_no_forbidden_outcomes(root: Path) -> list[str]:
    """No contract source may reference an excluded outcome category."""
    failures: list[str] = []
    checker_dir = Path(__file__).resolve().parent
    suffixes = {".toml", ".json", ".md"}
    ignored_parts = {
        ".git",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "site",
        ".ruff_cache",
        ".pytest_cache",
    }

    for path in sorted((root / "data").rglob("*")):
        if path.is_dir() or path.suffix not in suffixes:
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        # WHY: Skip the checks package itself, which names forbidden tokens.
        if checker_dir in path.resolve().parents:
            continue

        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_OUTCOME_TOKENS:
            if token in text:
                failures.append(f"forbidden outcome token {token!r} in {relative}")

    return failures


def check_entity_kinds(root: Path) -> list[str]:
    """The nine AE.* entity kinds must be present, ordered 1..9, fully described."""
    path = root / "data" / "entity-kinds" / "accountable_entity_kinds.toml"
    if not path.is_file():
        return ["missing data/entity-kinds/accountable_entity_kinds.toml"]

    try:
        data = _load_toml(path)
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid TOML in {path.name}: {exc}"]

    rows = data.get("accountable_entity_kinds")
    if not isinstance(rows, list):
        return ["entity kinds must define [[accountable_entity_kinds]] rows"]

    failures: list[str] = []
    seen_ids: set[str] = set()
    seen_orders: set[int] = set()

    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            failures.append(f"entity kind row {index} is not a table")
            continue

        entity_id = row.get("id")
        if not isinstance(entity_id, str) or not entity_id.startswith("AE."):
            failures.append(f"entity kind row {index} id must start with AE.")
        else:
            seen_ids.add(entity_id)

        order = row.get("order")
        if not isinstance(order, int):
            failures.append(f"entity kind row {index} missing integer order")
        else:
            seen_orders.add(order)

        for field_name in ("canonical_family", "canonical_profile", "label"):
            value = row.get(field_name)
            if not isinstance(value, str) or not value:
                failures.append(f"entity kind row {index} missing {field_name}")

    missing_ids = sorted(EXPECTED_ENTITY_KIND_IDS - seen_ids)
    extra_ids = sorted(seen_ids - EXPECTED_ENTITY_KIND_IDS)
    if missing_ids:
        failures.append(f"entity kinds missing ids: {', '.join(missing_ids)}")
    if extra_ids:
        failures.append(f"entity kinds has unexpected ids: {', '.join(extra_ids)}")

    if seen_orders != set(range(1, 10)):
        failures.append("entity kind orders must be exactly 1 through 9")

    return failures
