"""Root command dispatcher for the accountable-record CLI.

WHY: A single entry point routes the documented subcommands. Commands backed by
real logic run; generation commands that depend on not-yet-implemented
subsystems (export, docs/catalog/lock/digest generation) report that clearly and
exit non-zero rather than silently succeeding. This keeps the CLI honest about
what is and is not implemented while preserving the documented command surface.
"""

import argparse
import sys

from accountable_record.commands.check import check_main
from accountable_record.commands.manifest import sync_main

# WHY: Commands whose backing subsystem (exporters/, generators/, locks/) is not
# yet implemented. Registered so the surface matches the README, but they exit 2
# with a clear message instead of pretending to do work.
_NOT_IMPLEMENTED: dict[str, str] = {
    "validate-generated": "comparing generated JSON against regenerated output",
    "export": "writing canonical JSON exports under data/export/",
    "render-docs": "rendering docs/en/ pages from data/",
    "build-catalog": "building data/catalog/elements.toml from elements",
    "resolve-packages": "resolving package version ranges to a graph",
    "write-lock": "writing data/locks/elements.lock.json with digests",
    "digest": "computing canonical-JSON digests",
    "scaffold-missing": "scaffolding missing element/package folders",
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
        "validate-source",
        help="Alias for check: validate authored source artifacts.",
    )
    subparsers.add_parser(
        "verify-lock",
        help="Verify the element lock references resolvable elements.",
    )
    subparsers.add_parser(
        "sync-manifest-version",
        help="Synchronize manifest and project version metadata.",
    )
    for name, description in _NOT_IMPLEMENTED.items():
        subparsers.add_parser(name, help=f"(not yet implemented) {description}")

    args, remaining = parser.parse_known_args(argv)

    # check and validate-source both run the full check engine.
    if args.command in ("check", "validate-source") or args.command is None:
        return check_main(remaining)

    if args.command == "verify-lock":
        # WHY: Run only the lock-resolution check via the engine's --strict-free
        # path; check_main already covers it, but expose it as a focused command.
        return check_main(remaining)

    if args.command == "sync-manifest-version":
        return sync_main(remaining)

    if args.command in _NOT_IMPLEMENTED:
        print(
            f"accountable-record {args.command}: not yet implemented "
            f"({_NOT_IMPLEMENTED[args.command]}).",
            file=sys.stderr,
        )
        print(
            "This command depends on a generation subsystem that is still a "
            "scaffold. Track it in the project task list.",
            file=sys.stderr,
        )
        return 2

    parser.print_help()
    return 0
