"""Source-layout and parse checks for the actual repository layout.

WHY: The contract source of truth is ``data/`` (TOML) plus ``docs/en/`` (Markdown).
These checks validate that the files the contract depends on exist and parse,
using the layout this repository actually has -- not a legacy flat-file layout.
"""

import json
from pathlib import Path
import tomllib

# REQ: Root files the contract repository must carry. These exist in the repo;
# the check fails loudly if a future change removes one.
REQUIRED_ROOT_FILES = [
    "README.md",
    "MANIFEST.toml",
    "CITATION.cff",
    "DECISIONS.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "pyproject.toml",
]

# REQ: Narrative documentation entry points live under docs/en/ (data-first:
# docs explain data, they are not the source of truth). README lists these.
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

_IGNORED_PARTS = {
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


def _is_ignored(path: Path) -> bool:
    return any(part in _IGNORED_PARTS for part in path.parts)


def check_required_source_files(root: Path) -> list[str]:
    """Every required root file must exist."""
    failures: list[str] = []
    for relative in REQUIRED_ROOT_FILES:
        if not (root / relative).is_file():
            failures.append(f"missing required root file: {relative}")
    return failures


def check_required_docs(root: Path) -> list[str]:
    """Every required documentation entry point must exist."""
    failures: list[str] = []
    for relative in REQUIRED_DOCS:
        if not (root / relative).is_file():
            failures.append(f"missing required doc: {relative}")
    return failures


def check_toml_files_parse(root: Path) -> list[str]:
    """All TOML under data/ and the repo root must parse."""
    failures: list[str] = []
    for path in sorted(root.rglob("*.toml")):
        if _is_ignored(path):
            continue
        relative = path.relative_to(root).as_posix()
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            failures.append(f"invalid TOML in {relative}: {exc}")
    return failures


def check_json_files_parse(root: Path) -> list[str]:
    """All JSON under data/ and schemas/ must parse."""
    failures: list[str] = []
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
                failures.append(f"invalid JSON in {relative}: {exc}")
    return failures


def check_data_index(root: Path) -> list[str]:
    """data/index.toml source paths must exist; export keys must be declared."""
    path = root / "data" / "index.toml"
    if not path.is_file():
        return ["missing data/index.toml"]

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid TOML in data/index.toml: {exc}"]

    failures: list[str] = []

    source = data.get("source")
    if not isinstance(source, dict):
        failures.append("data/index.toml must define a [source] table")
    else:
        for key, value in source.items():
            if not isinstance(value, str):
                failures.append(f"data/index.toml source.{key} must be a string")
                continue
            if not (root / value).exists():
                failures.append(
                    f"data/index.toml source.{key} path does not exist: {value}"
                )

    export = data.get("export")
    if not isinstance(export, dict):
        failures.append("data/index.toml must define an [export] table")
    else:
        for required_key in ("index", "vocabulary", "component_groups", "elements"):
            if required_key not in export:
                failures.append(
                    f"data/index.toml export table missing key: {required_key}"
                )

    return failures
