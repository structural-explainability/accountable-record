"""AR interchange-schema presence/well-formedness checks, as kit Check records.

WHY: AR distributes JSON Schemas for its core interchange artifacts (bundle,
profile, report, claim, trait, component). These must exist, parse, and be
valid JSON Schema documents. AR-specific (it knows the six interchange schema
paths), so it lives in AR and is appended via registry.extend.

Converted from (root: Path) -> list[str] to the kit Check contract.
"""

from collections.abc import Iterable
import json

from se_contract_kit.resolution.context import ResolutionContext
from se_contract_kit.validation.registry import Check
from se_contract_kit.validation.results import CheckResult, failure, ok

__all__ = [
    "REQUIRED_INTERCHANGE_SCHEMAS",
    "check_required_schemas",
    "AR_SCHEMAS_CHECK",
]

CHECK_ID = "ar.schemas.interchange"

# REQ: Core interchange schemas every AR consumer needs.
REQUIRED_INTERCHANGE_SCHEMAS = [
    "schemas/bundle-1.json",
    "schemas/profile-1.json",
    "schemas/report-1.json",
    "schemas/claim-1.json",
    "schemas/trait-1.json",
    "schemas/component-1.json",
]


def _as_object_dict(value: object) -> dict[str, object] | None:
    """Return value as a string-keyed object dict if it is a dict, else None."""
    if not isinstance(value, dict):
        return None
    narrowed: dict[str, object] = {}
    for key, item in value.items():  # type: ignore[misc]
        narrowed[str(key)] = item  # type: ignore[index]
    return narrowed


def check_required_schemas(context: ResolutionContext) -> Iterable[CheckResult]:
    """Each interchange schema must exist, parse, and declare $schema."""
    root = context.repo_root
    results: list[CheckResult] = []

    for relative in REQUIRED_INTERCHANGE_SCHEMAS:
        path = root / relative
        if not path.is_file():
            results.append(failure(CHECK_ID, f"missing interchange schema: {relative}"))
            continue

        try:
            parsed: object = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            results.append(failure(CHECK_ID, f"invalid JSON in {relative}: {exc}"))
            continue

        data = _as_object_dict(parsed)
        if data is None:
            results.append(failure(CHECK_ID, f"{relative} must be a JSON object"))
            continue

        if "$schema" not in data:
            results.append(failure(CHECK_ID, f"{relative} missing $schema declaration"))

        if data.get("type") != "object":
            results.append(
                failure(CHECK_ID, f"{relative} top-level type should be 'object'")
            )

    return results or [ok(CHECK_ID, "all interchange schemas valid")]


AR_SCHEMAS_CHECK = Check(
    CHECK_ID, "AR interchange schemas valid", check_required_schemas
)
