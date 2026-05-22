"""Root command dispatcher for the accountable-record CLI.

WHY: A single entry point routes the documented subcommands. Commands backed by
real logic run; commands whose backing subsystem is intentionally not yet built
report that clearly and exit non-zero rather than silently succeeding.
"""

import argparse
import sys

from accountable_record.commands.check import check_main
from accountable_record.commands.generate import generate_main
from accountable_record.commands.manifest import sync_main

# WHY: These commands are intentionally registered so the documented CLI surface
# remains visible, but they must exit 2 until their backing subsystem exists.
_NOT_IMPLEMENTED: dict[str, str] = {
    "render-docs": "rendering docs/en/ pages from data/",
    "scaffold-missing": "scaffolding missing element/package folders",
}

_GENERATION_COMMANDS: set[str] = {
    "export",
    "validate-generated",
    "resolve-packages",
    "write-lock",
    "verify-lock",
    "build-catalog",
    "digest",
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
        "validate-source",
        help="Alias for check: validate authored source artifacts.",
    )
    subparsers.add_parser(
        "sync-manifest-version",
        help="Synchronize manifest and project version metadata.",
    )

    for name in sorted(_GENERATION_COMMANDS):
        subparsers.add_parser(name, help=f"Run generation command: {name}.")

    for name, description in _NOT_IMPLEMENTED.items():
        subparsers.add_parser(name, help=f"(not yet implemented) {description}")

    args, remaining = parser.parse_known_args(argv)

    if args.command in ("check", "validate-source") or args.command is None:
        return check_main(remaining)

    if args.command == "sync-manifest-version":
        return sync_main(remaining)

    if args.command in _GENERATION_COMMANDS:
        return generate_main([args.command, *remaining])

    if args.command in _NOT_IMPLEMENTED:
        print(
            f"accountable-record {args.command}: not yet implemented "
            f"({_NOT_IMPLEMENTED[args.command]}).",
            file=sys.stderr,
        )
        return 2

    parser.print_help()
    return 0
