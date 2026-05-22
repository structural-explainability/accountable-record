"""Check contract artifacts for internal consistency.

WHY: This command is the repository's self-consistency gate. It runs the check
engine (see :mod:`accountable_record.checks.engine`) against the *actual*
``data/`` + ``docs/en/`` layout and reports failures deterministically.

It is not the Accountable Record verifier implementation; it validates the
contract source in this repository, not external bundles.
"""

import argparse
from pathlib import Path
import sys

from accountable_record.checks import run_all_checks


def check_main(argv: list[str] | None = None) -> int:
    """Run repository-local contract consistency checks.

    Args:
        argv: Arguments after the ``check`` subcommand. ``None`` uses sys.argv.

    Returns:
        0 when all selected checks pass, 1 otherwise.
    """
    parser = argparse.ArgumentParser(
        prog="accountable-record check",
        description="Check accountable-record contract artifacts.",
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

    result = run_all_checks(args.root, strict_mode=args.strict)

    if not result.ok:
        for failure in result.failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        print(
            f"\n{len(result.failures)} failure(s) across "
            f"{len(result.checks_run)} check(s).",
            file=sys.stderr,
        )
        return 1

    print(
        f"OK: Accountable Record contract checks passed "
        f"({len(result.checks_run)} checks)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(check_main())
