"""Pipeline stage s050: build and validate the normalized catalog."""

from pathlib import Path

from accountable_record.ops.generators.artifacts import write_catalog
from accountable_record.pipeline.types import PipelineStageError, StageResult

STAGE_ID = "s050"
STAGE_CODE = "CA"
STAGE_TITLE = "Build and validate the normalized catalog"


def run(root: Path) -> StageResult:
    """Build data/catalog/elements.json."""
    result = write_catalog(root)
    if result.errors:
        raise PipelineStageError(STAGE_ID, STAGE_CODE, "; ".join(result.errors))

    return StageResult(
        STAGE_ID,
        STAGE_CODE,
        f"wrote data/catalog/elements.json with {result.count} element(s)",
    )
