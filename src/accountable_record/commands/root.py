"""Root command dispatcher for the accountable-record CLI.

WHY: A single entry point routes the documented subcommands.
Root owns the top-level command surface;
command-specific implementation stays in the command modules that own it.
"""

import argparse

from accountable_record.commands.check import check_main
from accountable_record.commands.generate import generate_main
from accountable_record.commands.manifest import sync_main
from accountable_record.commands.run import run_main

_GENERATION_COMMANDS: set[str] = {
    "export",
    "validate-generated",
    "resolve-packages",
    "write-lock",
    "verify-lock",
    "build-catalog",
    "digest",
    "render-docs",
}


def main(argv: list[str] | None = None) -> int:
    """Dispatch accountable-record subcommands.

    Args:
        argv: CLI arguments. ``None`` uses sys.argv.

    Returns:
        Process exit code.
    """
    parser = argparse.ArgumentParser(
        prog="accountable-record",
        description="Check and generate Accountable Record artifacts.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        metavar="command",
    )

    subparsers.add_parser(
        "check",
        help="Check contract artifacts for internal consistency.",
    )
    subparsers.add_parser(
        "run",
        help="Run staged Accountable Record pipeline stages.",
    )
    subparsers.add_parser(
        "sync-manifest-version",
        help="Synchronize manifest and project version metadata.",
    )
    subparsers.add_parser(
        "validate-source",
        help="Alias for check: validate authored source artifacts.",
    )

    for name in sorted(_GENERATION_COMMANDS):
        subparsers.add_parser(name, help=f"Run generation command: {name}.")

    args, remaining = parser.parse_known_args(argv)

    if args.command in ("check", "validate-source") or args.command is None:
        return check_main(remaining)

    if args.command == "run":
        return run_main(remaining)

    if args.command == "sync-manifest-version":
        return sync_main(remaining)

    if args.command in _GENERATION_COMMANDS:
        return generate_main([args.command, *remaining])

    parser.print_help()
    return 0
