"""Check Accountable Record contract artifacts for internal consistency.

WHY: This command is the repository's self-consistency gate. It loads the
repository's declarations, resolves its artifacts and dependencies into a
ResolutionContext, runs the Accountable Record check registry against it, and
reports the result deterministically.

It is not the Accountable Record verifier implementation; it validates the
contract source in this repository, not external bundles. Manifest schema
validation is delegated to se-manifest-schema; this command runs contract-kit
checks plus AR-specific repository consistency checks.
"""

import argparse
from pathlib import Path
import sys

from se_contract_kit.declarations.config import load_repo_config
from se_contract_kit.resolution.resolver import resolve_repo_config
from se_contract_kit.validation import run_checks

from accountable_record.ops.checks.engine import accountable_record_registry


def check_main(argv: list[str] | None = None) -> int:
    """Run repository-local contract consistency checks.

    Args:
        argv: Arguments after the ``check`` subcommand. ``None`` uses sys.argv.

    Returns:
        The check report exit code.
    """
    parser = argparse.ArgumentParser(
        prog="accountable-record check",
        description="Check Accountable Record contract artifacts.",
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

    repo_root = args.root if args.root is not None else Path.cwd()
    config = load_repo_config(repo_root=repo_root)
    context = resolve_repo_config(repo_root=repo_root, config=config)

    registry = accountable_record_registry()
    report = run_checks(registry=registry, context=context, strict=args.strict)

    if not report.passed:
        for failure_item in report.failures:
            location = (
                f" [{failure_item.artifact_id}]" if failure_item.artifact_id else ""
            )
            print(
                f"FAIL ({failure_item.check_id}){location}: {failure_item.message}",
                file=sys.stderr,
            )
        print(
            f"\n{len(report.failures)} failure(s) across "
            f"{len(report.results)} result(s); overall status "
            f"{report.overall_status.value}.",
            file=sys.stderr,
        )
        return report.exit_code

    print(
        f"OK: Accountable Record contract checks passed "
        f"({len(registry.checks)} checks, {len(report.results)} results)."
    )
    return report.exit_code


if __name__ == "__main__":
    raise SystemExit(check_main())
