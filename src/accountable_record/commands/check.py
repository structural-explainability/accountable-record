"""Check contract artifacts for internal consistency."""

import argparse
import json
from pathlib import Path
import sys
import tomllib
from typing import Any

OUTCOME_VALUES = {
    "pass",
    "fail",
    "partial",
    "cannot-verify",
}

FORBIDDEN_TEXT = [
    "AR.KIND.",
    "AR.TRANSFORM.NOT_APPLICABLE",
    "Outcome.INAPPLICABLE",
    '"outcome": "inapplicable"',
    '"inapplicable"',
]

REQUIRED_SCHEMA_FILES = [
    "schemas/bundle-1.json",
    "schemas/profile-1.json",
    "schemas/report-1.json",
    "schemas/claim-1.json",
    "schemas/trait-1.json",
]

REQUIRED_ROOT_FILES = [
    "SE_MANIFEST.toml",
    "README.md",
    "SPEC.md",
    "IDENTIFIERS.md",
    "CONFORMANCE.md",
    "ADOPTION_LEVELS.md",
    "ENTITY_KINDS.md",
    "TRAITS.md",
    "CLAIMS.md",
    "EXPORT_CONTRACT.md",
    "VERIFICATION_MODEL.md",
    "TRANSFORMATION_MODEL.md",
    "NON_GOALS.md",
    "SCOPE.md",
    "WHEN_TO_USE_AR.md",
    "DECISIONS.md",
    "CITATION.cff",
]


def check_main(argv: list[str] | None = None) -> int:
    """Run repository-local contract consistency checks."""
    parser = argparse.ArgumentParser(
        description="Check accountable-record contract artifacts."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Run additional stricter checks when available.",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    failures: list[str] = []

    failures.extend(_check_required_files(root))
    failures.extend(_check_json_schemas_parse(root))
    failures.extend(_check_toml_files_parse(root))
    failures.extend(_check_entity_kind_metadata(root))
    failures.extend(_check_report_schema_outcomes(root))
    failures.extend(_check_forbidden_text(root))

    if args.strict:
        failures.extend(_check_manifest_basic_shape(root))

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    print("OK: Accountable Record contract checks passed.")
    return 0


def _check_required_files(root: Path) -> list[str]:
    failures: list[str] = []

    for relative_path in REQUIRED_ROOT_FILES + REQUIRED_SCHEMA_FILES:
        path = root / relative_path
        if not path.is_file():
            failures.append(f"missing required file: {relative_path}")

    return failures


def _check_json_schemas_parse(root: Path) -> list[str]:
    failures: list[str] = []

    for relative_path in REQUIRED_SCHEMA_FILES:
        path = root / relative_path
        if not path.is_file():
            continue

        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid JSON in {relative_path}: {exc}")

    return failures


def _check_toml_files_parse(root: Path) -> list[str]:
    failures: list[str] = []

    for path in sorted(root.rglob("*.toml")):
        if _is_ignored_path(path):
            continue

        relative_path = path.relative_to(root).as_posix()
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            failures.append(f"invalid TOML in {relative_path}: {exc}")

    return failures


def _check_entity_kind_metadata(root: Path) -> list[str]:
    failures: list[str] = []
    path = root / "data" / "entity-kinds" / "accountable_entity_kinds.toml"

    if not path.is_file():
        failures.append(
            "missing entity kind metadata: data/entity-kinds/accountable_entity_kinds.toml"
        )
        return failures

    try:
        parsed = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid TOML in {path.relative_to(root).as_posix()}: {exc}"]

    rows = parsed.get("accountable_entity_kinds")
    if not isinstance(rows, list):
        return ["entity kind metadata must define [[accountable_entity_kinds]] rows"]

    expected_ids = {
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

    seen_ids: set[str] = set()
    seen_orders: set[int] = set()

    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            failures.append(f"entity kind row {index} is not a TOML table")
            continue

        entity_id = row.get("id")
        order = row.get("order")
        canonical_family = row.get("canonical_family")
        canonical_profile = row.get("canonical_profile")

        if not isinstance(entity_id, str):
            failures.append(f"entity kind row {index} missing string id")
        elif not entity_id.startswith("AE."):
            failures.append(
                f"entity kind row {index} id must start with AE.: {entity_id}"
            )
        else:
            seen_ids.add(entity_id)

        if not isinstance(order, int):
            failures.append(f"entity kind row {index} missing integer order")
        else:
            seen_orders.add(order)

        if not isinstance(canonical_family, str) or not canonical_family:
            failures.append(f"entity kind row {index} missing canonical_family")

        if not isinstance(canonical_profile, str) or not canonical_profile:
            failures.append(f"entity kind row {index} missing canonical_profile")

    missing_ids = sorted(expected_ids - seen_ids)
    extra_ids = sorted(seen_ids - expected_ids)

    if missing_ids:
        failures.append(f"entity kind metadata missing ids: {', '.join(missing_ids)}")
    if extra_ids:
        failures.append(
            f"entity kind metadata has unexpected ids: {', '.join(extra_ids)}"
        )

    expected_orders = set(range(1, 10))
    if seen_orders != expected_orders:
        failures.append("entity kind metadata orders must be exactly 1 through 9")

    return failures


def _check_report_schema_outcomes(root: Path) -> list[str]:
    path = root / "schemas" / "report-1.json"
    if not path.is_file():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    serialized = json.dumps(data, sort_keys=True)
    failures: list[str] = []

    for outcome in OUTCOME_VALUES:
        if outcome not in serialized:
            failures.append(
                f"report schema does not mention required outcome: {outcome}"
            )

    if "inapplicable" in serialized:
        failures.append("report schema must not include inapplicable as an outcome")

    return failures


def _check_forbidden_text(root: Path) -> list[str]:
    failures: list[str] = []

    suffixes = {".md", ".toml", ".json", ".py"}
    checker_path = Path(__file__).resolve()

    for path in sorted(root.rglob("*")):
        if path.resolve() == checker_path:
            continue

        if path.is_dir() or path.suffix not in suffixes or _is_ignored_path(path):
            continue

        if (
            path.relative_to(root).as_posix()
            == "src/accountable_record/commands/check.py"
        ):
            continue

        relative_path = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")

        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                failures.append(
                    f"forbidden text {forbidden!r} found in {relative_path}"
                )

    return failures


def _check_manifest_basic_shape(root: Path) -> list[str]:
    path = root / "SE_MANIFEST.toml"
    if not path.is_file():
        return []

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError:
        return []

    failures: list[str] = []

    repo = _table(data, "repo")
    if repo.get("name") != "accountable-record":
        failures.append("SE_MANIFEST.toml repo.name must be accountable-record")

    if repo.get("kind") != "contract":
        failures.append("SE_MANIFEST.toml repo.kind must be contract")

    layer = _table(data, "layer")
    if layer.get("role") != "accountable-record-language-neutral-contract":
        failures.append(
            "SE_MANIFEST.toml layer.role must be accountable-record-language-neutral-contract"
        )

    return failures


def _table(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if isinstance(value, dict):
        return value
    return {}


def _is_ignored_path(path: Path) -> bool:
    ignored_parts = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "site",
    }
    return any(part in ignored_parts for part in path.parts)


if __name__ == "__main__":
    raise SystemExit(check_main())
