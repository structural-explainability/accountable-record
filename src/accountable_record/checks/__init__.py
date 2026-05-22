"""Cross-artifact consistency checks for Accountable Record source and generated artifacts.

This package provides the check engine that powers ``accountable-record check``.
Each check module exposes one or more functions that take the repository root
and return a list of failure strings. The engine in
:mod:`accountable_record.checks.engine` aggregates them.

WHY: Checks validate the *actual* ``data/`` + ``docs/en/`` layout of this
repository, not a legacy flat-file layout. The contract source of truth lives
under ``data/`` (see DECISIONS.md and the data-first principle in README.md).
"""

from accountable_record.checks.engine import (
    CheckResult,
    run_all_checks,
)

__all__ = [
    "CheckResult",
    "run_all_checks",
]
