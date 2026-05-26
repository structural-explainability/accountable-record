"""Generation command dispatcher for the accountable-record CLI.

WHY: Root command parsing should only route command names. This module owns the
generation command surface and adapts CLI calls to exporter, resolver,
generator, and validator subsystems.
"""

import argparse
from collections.abc import Callable
from pathlib import Path

from accountable_record.ops.exporters.data_export import run_export
from accountable_record.ops.generators.artifacts import write_catalog
from accountable_record.ops.generators.docs import render_reference_docs
from accountable_record.ops.generators.lock import verify_lock, write_lock
from accountable_record.ops.resolvers.packages import resolve_packages
from accountable_record.ops.resolvers.versions import digest_toml_file
from accountable_record.ops.validators.generated import validate_generated

CommandMain = Callable[[list[str]], int]


def _print_errors(errors: list[str]) -> None:
    for error in errors:
        print(f"ERROR: {error}")


def _export_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="accountable-record export",
        description="Export authored TOML artifacts to canonical JSON.",
    )
    parser.parse_args(argv)

    result = run_export(Path.cwd(), write=True)
    if result.errors:
        _print_errors(result.errors)
        return 1

    print(f"Exported {len(result.written)} files.")
    return 0


def _validate_generated_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="accountable-record validate-generated",
        description="Compare committed generated JSON against regenerated output.",
    )
    parser.parse_args(argv)

    result = validate_generated(Path.cwd())
    if result.failures:
        _print_errors(result.failures)
        return 1

    print(f"Generated artifacts are current ({result.compared} files compared).")
    return 0


def _resolve_packages_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="accountable-record resolve-packages",
        description="Resolve package element references and detect conflicts.",
    )
    parser.parse_args(argv)

    result = resolve_packages(Path.cwd())
    if result.errors:
        _print_errors(result.errors)
        return 1

    print(
        f"Resolved {len(result.packages)} packages "
        f"to {len(result.elements)} unique elements."
    )
    return 0


def _write_lock_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="accountable-record write-lock",
        description="Write data/locks/elements.lock.json.",
    )
    parser.parse_args(argv)

    result = write_lock(Path.cwd())
    if result.errors:
        _print_errors(result.errors)
        return 1

    print("Wrote data/locks/elements.lock.json.")
    return 0


def _verify_lock_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="accountable-record verify-lock",
        description="Verify the committed lock against a fresh package resolution.",
    )
    parser.parse_args(argv)

    result = verify_lock(Path.cwd())
    if result.failures:
        _print_errors(result.failures)
        return 1

    print("Lock is current.")
    return 0


def _build_catalog_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="accountable-record build-catalog",
        description="Build data/catalog/elements.json.",
    )
    parser.parse_args(argv)

    result = write_catalog(Path.cwd())
    if result.errors:
        _print_errors(result.errors)
        return 1

    print(f"Wrote data/catalog/elements.json with {result.count} elements.")
    return 0


def _digest_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="accountable-record digest",
        description="Print sha256 digests for package and element TOML as canonical JSON.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional TOML files to digest. Defaults to package and element sources.",
    )
    args = parser.parse_args(argv)

    root = Path.cwd()

    if args.paths:
        paths = [Path(path) for path in args.paths]
    else:
        paths = [
            *sorted((root / "data" / "packages").glob("*/package.toml")),
            *sorted((root / "data" / "elements").glob("*/*/element.toml")),
        ]

    for path in paths:
        digest = digest_toml_file(path)
        print(f"{digest}  {path.as_posix()}")

    return 0


def _render_docs_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="accountable-record render-docs",
        description="Render generated reference Markdown from contract data.",
    )
    parser.parse_args(argv)

    result = render_reference_docs(Path.cwd())
    if result.errors:
        _print_errors(result.errors)
        return 1

    print(f"Rendered {len(result.written)} reference docs.")
    return 0


_COMMANDS: dict[str, CommandMain] = {
    "export": _export_main,
    "validate-generated": _validate_generated_main,
    "resolve-packages": _resolve_packages_main,
    "write-lock": _write_lock_main,
    "verify-lock": _verify_lock_main,
    "build-catalog": _build_catalog_main,
    "digest": _digest_main,
    "render-docs": _render_docs_main,
}


def generate_main(argv: list[str] | None = None) -> int:
    """Dispatch implemented generation subcommands.

    Args:
        argv: Generation command arguments, beginning with the command name.

    Returns:
        Process exit code.
    """
    parser = argparse.ArgumentParser(
        prog="accountable-record",
        description="Generate and verify Accountable Record artifacts.",
    )
    parser.add_argument("command", choices=sorted(_COMMANDS))

    args, remaining = parser.parse_known_args(argv)
    return _COMMANDS[args.command](remaining)
