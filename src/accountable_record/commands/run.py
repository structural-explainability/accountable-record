"""CLI adapter for the staged Accountable Record pipeline."""

import argparse
from pathlib import Path

from accountable_record.pipeline.registry import STAGE_BY_ID
from accountable_record.pipeline.runner import run_all, run_stage


def run_main(argv: list[str] | None = None) -> int:
    """Run one stage or the full Accountable Record pipeline."""
    parser = argparse.ArgumentParser(
        prog="accountable-record run",
        description="Run staged Accountable Record pipeline checks and generators.",
    )
    parser.add_argument(
        "stage",
        choices=["all", *sorted(STAGE_BY_ID)],
        help="Stage to run, or 'all' for the full pipeline.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current working directory.",
    )
    args = parser.parse_args(argv)

    if args.stage == "all":
        return run_all(args.root)

    return run_stage(args.stage, args.root)
