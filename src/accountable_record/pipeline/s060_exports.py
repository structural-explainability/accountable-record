"""Pipeline stage s060: write machine-readable exports."""

from pathlib import Path

from accountable_record.ops.exporters.data_export import run_export
from accountable_record.pipeline.types import PipelineStageError, StageResult

STAGE_ID = "s060"
STAGE_CODE = "EX"
STAGE_TITLE = "Write and validate machine-readable exports"


def run(root: Path) -> StageResult:
    """Export authored TOML artifacts to canonical JSON."""
    result = run_export(root, write=True)
    if result.errors:
        raise PipelineStageError(STAGE_ID, STAGE_CODE, "; ".join(result.errors))

    return StageResult(
        STAGE_ID,
        STAGE_CODE,
        f"exported {len(result.written)} machine-readable artifact(s)",
    )
