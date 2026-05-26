"""Progressive-record maturity checks, as a kit Check record.

WHY (AR-D-005): AR conformance is incremental and levels are nested. The
progressive sample records under ``data/records/progressive/`` illustrate each
maturity level. This check confirms each ``level-N.json`` declares a
``maturity_level`` equal to N and that the set of levels is contiguous from 0,
so the incremental-conformance story stays internally consistent. AR-specific;
appended to the kit registry via registry.extend.

Converted from (root: Path) -> list[str] to the kit Check contract.
"""

from collections.abc import Iterable
import json

from se_contract_kit.resolution.context import ResolutionContext
from se_contract_kit.validation.registry import Check
from se_contract_kit.validation.results import CheckResult, cannot_verify, failure, ok

__all__ = ["CHECK_ID", "check_record_maturity_levels", "RECORD_MATURITY_CHECK"]

CHECK_ID = "ar.records.maturity-levels"


def check_record_maturity_levels(context: ResolutionContext) -> Iterable[CheckResult]:
    """Progressive records must declare maturity_level matching their filename."""
    root = context.repo_root
    records_dir = root / "data" / "records" / "progressive"
    if not records_dir.is_dir():
        return [cannot_verify(CHECK_ID, "missing data/records/progressive/ directory")]

    record_files = sorted(records_dir.glob("level-*.json"))
    if not record_files:
        return [
            cannot_verify(
                CHECK_ID, "data/records/progressive/ contains no level-*.json files"
            )
        ]

    results: list[CheckResult] = []
    seen_levels: set[int] = set()

    for path in record_files:
        relative = path.relative_to(root).as_posix()

        # Filename encodes the level: level-2.json -> 2
        parts = path.stem.rsplit("-", 1)
        if len(parts) != 2 or not parts[1].isdigit():
            results.append(
                failure(CHECK_ID, f"{relative} filename does not encode a level")
            )
            continue
        file_level = int(parts[1])

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            results.append(failure(CHECK_ID, f"invalid JSON in {relative}: {exc}"))
            continue

        declared = data.get("maturity_level")
        if declared != file_level:
            results.append(
                failure(
                    CHECK_ID,
                    f"{relative} declares maturity_level {declared!r}, expected {file_level}",
                )
            )
        else:
            seen_levels.add(file_level)

        if "elements" not in data:
            results.append(failure(CHECK_ID, f"{relative} missing elements array"))

    if seen_levels:
        expected = set(range(0, max(seen_levels) + 1))
        gap = sorted(expected - seen_levels)
        if gap:
            results.append(
                failure(
                    CHECK_ID,
                    f"progressive records missing levels: {', '.join(str(n) for n in gap)}",
                )
            )

    return results or [
        ok(CHECK_ID, f"{len(record_files)} progressive record(s) consistent")
    ]


RECORD_MATURITY_CHECK = Check(
    CHECK_ID, "Record maturity levels valid", check_record_maturity_levels
)
