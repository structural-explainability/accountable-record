"""Schema presence and well-formedness checks.

WHY: AR distributes JSON Schemas for its core interchange artifacts (bundle,
profile, report, claim, trait, component). The README badges and the identity
contract depend on these existing and being valid JSON Schema documents.

OBS: This check validates the six top-level interchange schemas under
``schemas/``. The larger per-artifact schema set under ``data/schemas/`` is
validated for parse-ability by the source checks; enforcing a declared-id ->
file mapping there is deferred (some declared ids are internal index schemas
that intentionally have no standalone file).
"""

import json
from pathlib import Path

# REQ: Core interchange schemas every AR consumer needs.
REQUIRED_INTERCHANGE_SCHEMAS = [
    "schemas/bundle-1.json",
    "schemas/profile-1.json",
    "schemas/report-1.json",
    "schemas/claim-1.json",
    "schemas/trait-1.json",
    "schemas/component-1.json",
]


def check_required_schemas(root: Path) -> list[str]:
    """Each interchange schema must exist, parse, and declare $schema."""
    failures: list[str] = []

    for relative in REQUIRED_INTERCHANGE_SCHEMAS:
        path = root / relative
        if not path.is_file():
            failures.append(f"missing interchange schema: {relative}")
            continue

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid JSON in {relative}: {exc}")
            continue

        if not isinstance(data, dict):
            failures.append(f"{relative} must be a JSON object")
            continue

        if "$schema" not in data:
            failures.append(f"{relative} missing $schema declaration")

        if data.get("type") != "object":
            failures.append(f"{relative} top-level type should be 'object'")

    return failures
