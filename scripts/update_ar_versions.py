"""Update AR package and element TOML versions for a release.

Run from the repository root:

    uv run python scripts/update_ar_versions.py 0.3.0
"""

from __future__ import annotations

import argparse
from pathlib import Path

VERSION_PREFIX = 'version = "'


def update_version_line(path: Path, version: str) -> bool:
    """Update the first top-level TOML version line in a file."""
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)

    changed = False
    updated: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not changed and stripped.startswith(VERSION_PREFIX):
            newline = "\n" if line.endswith("\n") else ""
            updated.append(f'{VERSION_PREFIX}{version}"{newline}')
            changed = True
        else:
            updated.append(line)

    if not changed:
        raise ValueError(f"No version line found in {path}")

    new_text = "".join(updated)
    if new_text != original:
        path.write_text(new_text, encoding="utf-8")
        return True

    return False


def main() -> int:
    """Update package and element versions."""
    parser = argparse.ArgumentParser()
    parser.add_argument("version", help="Release version, for example 0.3.0")
    args = parser.parse_args()

    root = Path.cwd()

    paths = [
        *sorted((root / "data" / "packages").glob("*/package.toml")),
        *sorted((root / "data" / "elements").glob("*/*/element.toml")),
    ]

    if not paths:
        raise SystemExit("No package or element TOML files found.")

    changed_count = 0
    for path in paths:
        if update_version_line(path, args.version):
            changed_count += 1
            print(f"updated {path.as_posix()}")

    print(f"Updated {changed_count} of {len(paths)} files to {args.version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
