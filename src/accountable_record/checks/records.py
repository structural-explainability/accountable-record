"""Progressive-record maturity checks.

WHY (AR-D-005): AR conformance is incremental and levels are nested. The
progressive sample records under ``data/records/progressive/`` illustrate each
maturity level. This check confirms each ``level-N.json`` declares a
``maturity_level`` equal to N and that the set of levels is contiguous from 0,
so the incremental-conformance story stays internally consistent.
"""

import json
from pathlib import Path


def check_record_maturity_levels(root: Path) -> list[str]:
    """Progressive records must declare maturity_level matching their filename."""
    records_dir = root / "data" / "records" / "progressive"
    if not records_dir.is_dir():
        return ["missing data/records/progressive/ directory"]

    record_files = sorted(records_dir.glob("level-*.json"))
    if not record_files:
        return ["data/records/progressive/ contains no level-*.json files"]

    failures: list[str] = []
    seen_levels: set[int] = set()

    for path in record_files:
        relative = path.relative_to(root).as_posix()

        # Filename encodes the level: level-2.json -> 2
        stem = path.stem  # e.g. "level-2"
        parts = stem.rsplit("-", 1)
        if len(parts) != 2 or not parts[1].isdigit():
            failures.append(f"{relative} filename does not encode a level")
            continue
        file_level = int(parts[1])

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid JSON in {relative}: {exc}")
            continue

        declared = data.get("maturity_level")
        if declared != file_level:
            failures.append(
                f"{relative} declares maturity_level {declared!r}, "
                f"expected {file_level}"
            )
        else:
            seen_levels.add(file_level)

        if "elements" not in data:
            failures.append(f"{relative} missing elements array")

    # Levels should be contiguous starting at 0.
    if seen_levels:
        expected = set(range(0, max(seen_levels) + 1))
        missing = sorted(expected - seen_levels)
        if missing:
            failures.append(
                f"progressive records missing levels: "
                f"{', '.join(str(level) for level in missing)}"
            )

    return failures
