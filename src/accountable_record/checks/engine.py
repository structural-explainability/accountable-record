"""Check engine: aggregate individual consistency checks into one result.

WHY: The CLI needs a single place that knows the ordered set of checks, runs
them against a repository root, and reports failures deterministically. Keeping
the registry here (rather than in the CLI command) lets tests exercise the
engine directly without going through argument parsing.

Each registered check is a callable ``(root: Path) -> list[str]`` returning a
list of human-readable failure messages. An empty list means the check passed.
Strict-only checks run only when ``strict=True`` is requested.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from accountable_record.checks import (
    component_groups,
    conformance,
    contracts,
    elements,
    namespace,
    records,
    schemas,
    source,
    strict,
)

# A check takes the repository root and returns failure messages.
Check = Callable[[Path], list[str]]


@dataclass(frozen=True)
class CheckResult:
    """Structured outcome of running the check engine.

    Attributes:
        failures: Ordered failure messages. Empty means everything passed.
        checks_run: Names of the checks that executed, in order.
    """

    failures: list[str] = field(default_factory=list)
    checks_run: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """Return True when no checks failed."""
        return not self.failures


# WHY: Ordered so the most foundational problems (missing required source files,
# unparseable TOML/JSON) surface before higher-level cross-reference failures.
# REQ: Names are stable; CI logs and tests reference them.
_BASE_CHECKS: list[tuple[str, Check]] = [
    ("required-source-files", source.check_required_source_files),
    ("toml-parses", source.check_toml_files_parse),
    ("json-parses", source.check_json_files_parse),
    ("required-docs", source.check_required_docs),
    ("data-index", source.check_data_index),
    ("schemas", schemas.check_required_schemas),
    ("conformance-outcomes", conformance.check_outcomes_closed),
    ("conformance-no-forbidden-outcomes", conformance.check_no_forbidden_outcomes),
    ("entity-kinds", conformance.check_entity_kinds),
    ("component-groups", component_groups.check_group_index_resolves),
    ("elements", elements.check_element_identity_consistency),
    ("element-lock", elements.check_lock_references_resolve),
    ("namespace", namespace.check_authority_aliases_resolve),
    ("contracts", contracts.check_identity_contract_shape),
    ("records-maturity", records.check_record_maturity_levels),
]

_STRICT_CHECKS: list[tuple[str, Check]] = [
    ("strict-manifest", strict.check_manifest_shape),
    ("strict-no-todo-in-elements", strict.check_no_todo_in_released_elements),
    ("strict-docs-cover-groups", strict.check_docs_cover_component_groups),
]


def run_all_checks(root: Path, *, strict_mode: bool = False) -> CheckResult:
    """Run every registered check against ``root``.

    Args:
        root: Repository root to validate.
        strict_mode: When True, also run the stricter checks.

    Returns:
        A :class:`CheckResult` with aggregated failures and the names of the
        checks that ran.
    """
    resolved = root.resolve()

    selected = list(_BASE_CHECKS)
    if strict_mode:
        selected += _STRICT_CHECKS

    failures: list[str] = []
    checks_run: list[str] = []

    for name, check in selected:
        checks_run.append(name)
        try:
            check_failures = check(resolved)
        except Exception as exc:  # noqa: BLE001
            # WHY: A crashing check is itself a failure to report, not a reason
            # to abort the whole run; surface it and continue.
            failures.append(f"[{name}] check raised {type(exc).__name__}: {exc}")
            continue

        failures.extend(f"[{name}] {message}" for message in check_failures)

    return CheckResult(failures=failures, checks_run=checks_run)
