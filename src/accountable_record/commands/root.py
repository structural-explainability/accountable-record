"""Root command dispatcher for the accountable-record CLI."""

import argparse

from accountable_record.commands.check import check_main
from accountable_record.commands.manifest import sync_main


def main(argv: list[str] | None = None) -> int:
    """Dispatch accountable-record subcommands."""
    parser = argparse.ArgumentParser(
        prog="accountable-record",
        description="Check contract artifacts for internal consistency.",
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
        "sync-manifest-version",
        help="Synchronize manifest and project version metadata.",
    )

    args, remaining = parser.parse_known_args(argv)

    if args.command == "check" or args.command is None:
        return check_main(remaining)

    if args.command == "sync-manifest-version":
        return sync_main(remaining)

    parser.print_help()
    return 0
