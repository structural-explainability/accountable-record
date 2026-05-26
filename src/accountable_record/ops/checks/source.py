"""AR source-layout and parse checks, as kit Check records.

WHY: AR's contract source of truth is data/ (TOML) plus docs/en/ (Markdown).
These checks validate that the files AR depends on exist and parse, against
AR's actual layout. They are AR-specific (they know AR's required files, docs,
and data/index.toml shape), so they live in AR and are appended to the kit
registry via registry.extend.

Converted from the legacy (root: Path) -> list[str] engine signature to the
kit Check contract: (ResolutionContext) -> Iterable[CheckResult].
"""

from collections.abc import Iterable
import json
from pathlib import Path
import tomllib

from se_contract_kit.resolution.context import ResolutionContext
from se_contract_kit.validation.registry import Check
from se_contract_kit.validation.results import CheckResult, failure, ok

__all__ = [
    "REQUIRED_ROOT_FILES",
    "REQUIRED_DOCS",
    "REQUIRED_SOURCE_FILES_CHECK",
    "REQUIRED_DOCS_CHECK",
    "TOML_PARSES_CHECK",
    "JSON_PARSES_CHECK",
    "DATA_INDEX_CHECK",
    "AR_SOURCE_CHECKS",
    "check_required_source_files",
    "check_required_docs",
    "check_toml_files_parse",
    "check_json_files_parse",
    "check_data_index",
]

# REQ: Root files the contract repository must carry.
REQUIRED_ROOT_FILES = [
    "README.md",
    "SE_MANIFEST.toml",
    "CITATION.cff",
    "DECISIONS.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "pyproject.toml",
]

# REQ: Narrative documentation entry points under docs/en/.
REQUIRED_DOCS = [
    "docs/en/scope.md",
    "docs/en/when-to-use-ar.md",
    "docs/en/non-goals.md",
    "docs/en/subjects.md",
    "docs/en/claims.md",
    "docs/en/traits.md",
    "docs/en/conformance.md",
    "docs/en/verification.md",
    "docs/en/exports.md",
    "docs/en/transformations.md",
    "docs/en/failure-modes.md",
]

_IGNORED_PARTS = frozenset(
    {
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
)

REQUIRED_SOURCE_FILES_ID = "ar.source.required-files"
REQUIRED_DOCS_ID = "ar.source.required-docs"
TOML_PARSES_ID = "ar.source.toml-parses"
JSON_PARSES_ID = "ar.source.json-parses"
DATA_INDEX_ID = "ar.source.data-index"


def check_required_source_files(context: ResolutionContext) -> Iterable[CheckResult]:
    """Every required root file must exist."""
    root = context.repo_root
    results: list[CheckResult] = [
        failure(REQUIRED_SOURCE_FILES_ID, f"missing required root file: {rel}")
        for rel in REQUIRED_ROOT_FILES
        if not (root / rel).is_file()
    ]
    return results or [ok(REQUIRED_SOURCE_FILES_ID, "all required root files present")]


def check_required_docs(context: ResolutionContext) -> Iterable[CheckResult]:
    """Every required documentation entry point must exist."""
    root = context.repo_root
    results: list[CheckResult] = [
        failure(REQUIRED_DOCS_ID, f"missing required doc: {rel}")
        for rel in REQUIRED_DOCS
        if not (root / rel).is_file()
    ]
    return results or [ok(REQUIRED_DOCS_ID, "all required docs present")]


def check_toml_files_parse(context: ResolutionContext) -> Iterable[CheckResult]:
    """All TOML under the repo (minus ignored dirs) must parse."""
    root = context.repo_root
    results: list[CheckResult] = []
    for path in sorted(root.rglob("*.toml")):
        if _is_ignored(path):
            continue
        relative = path.relative_to(root).as_posix()
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            results.append(
                failure(TOML_PARSES_ID, f"invalid TOML in {relative}: {exc}")
            )
    return results or [ok(TOML_PARSES_ID, "all TOML parses")]


def check_json_files_parse(context: ResolutionContext) -> Iterable[CheckResult]:
    """All JSON under data/ and schemas/ must parse."""
    root = context.repo_root
    results: list[CheckResult] = []
    for base in ("data", "schemas"):
        base_dir = root / base
        if not base_dir.is_dir():
            continue
        for path in sorted(base_dir.rglob("*.json")):
            if _is_ignored(path):
                continue
            relative = path.relative_to(root).as_posix()
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                results.append(
                    failure(JSON_PARSES_ID, f"invalid JSON in {relative}: {exc}")
                )
    return results or [ok(JSON_PARSES_ID, "all JSON parses")]


def check_data_index(context: ResolutionContext) -> Iterable[CheckResult]:
    """data/index.toml source paths must exist; export keys must be declared."""
    root = context.repo_root
    path = root / "data" / "index.toml"
    if not path.is_file():
        return [failure(DATA_INDEX_ID, "missing data/index.toml")]

    try:
        parsed: object = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return [failure(DATA_INDEX_ID, f"invalid TOML in data/index.toml: {exc}")]

    data = _as_object_dict(parsed)
    if data is None:
        return [failure(DATA_INDEX_ID, "data/index.toml is not a table")]

    results: list[CheckResult] = []

    source = _as_object_dict(data.get("source"))
    if source is None:
        results.append(
            failure(DATA_INDEX_ID, "data/index.toml must define a [source] table")
        )
    else:
        for key, value in source.items():
            if not isinstance(value, str):
                results.append(
                    failure(
                        DATA_INDEX_ID,
                        f"data/index.toml source.{key} must be a string",
                    )
                )
                continue
            if not (root / value).exists():
                results.append(
                    failure(
                        DATA_INDEX_ID,
                        f"data/index.toml source.{key} path does not exist: {value}",
                    )
                )

    export = _as_object_dict(data.get("export"))
    if export is None:
        results.append(
            failure(DATA_INDEX_ID, "data/index.toml must define an [export] table")
        )
    else:
        for required_key in ("index", "vocabulary", "component_groups", "elements"):
            if required_key not in export:
                results.append(
                    failure(
                        DATA_INDEX_ID,
                        f"data/index.toml export table missing key: {required_key}",
                    )
                )

    return results or [ok(DATA_INDEX_ID, "data/index.toml source and export valid")]


REQUIRED_SOURCE_FILES_CHECK = Check(
    REQUIRED_SOURCE_FILES_ID, "Required root files exist", check_required_source_files
)
REQUIRED_DOCS_CHECK = Check(
    REQUIRED_DOCS_ID, "Required docs exist", check_required_docs
)
TOML_PARSES_CHECK = Check(TOML_PARSES_ID, "All TOML parses", check_toml_files_parse)
JSON_PARSES_CHECK = Check(JSON_PARSES_ID, "All JSON parses", check_json_files_parse)
DATA_INDEX_CHECK = Check(DATA_INDEX_ID, "data/index.toml valid", check_data_index)

AR_SOURCE_CHECKS: tuple[Check, ...] = (
    REQUIRED_SOURCE_FILES_CHECK,
    REQUIRED_DOCS_CHECK,
    TOML_PARSES_CHECK,
    JSON_PARSES_CHECK,
    DATA_INDEX_CHECK,
)


def _is_ignored(path: Path) -> bool:
    return any(part in _IGNORED_PARTS for part in path.parts)


def _as_object_dict(value: object) -> dict[str, object] | None:
    """Return value as a string-keyed object dict if it is a dict, else None."""
    if not isinstance(value, dict):
        return None
    narrowed: dict[str, object] = {}
    for key, item in value.items():  # type: ignore[misc]
        narrowed[str(key)] = item  # type: ignore[index]
    return narrowed
