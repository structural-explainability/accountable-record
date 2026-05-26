"""Pipeline stage s090: verify final contract state."""

from pathlib import Path

from accountable_record.ops.generators.lock import verify_lock
from accountable_record.pipeline.types import PipelineStageError, StageResult

STAGE_ID = "s090"
STAGE_CODE = "VF"
STAGE_TITLE = "Verify final contract state"


def run(root: Path) -> StageResult:
    """Verify the committed lock against a fresh package resolution."""
    result = verify_lock(root)
    if result.failures:
        raise PipelineStageError(STAGE_ID, STAGE_CODE, "; ".join(result.failures))

    return StageResult(STAGE_ID, STAGE_CODE, "lock is current")
