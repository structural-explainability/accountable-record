"""Pipeline stage s070: resolve packages and write lock material."""

from pathlib import Path

from accountable_record.ops.generators.lock import write_lock
from accountable_record.ops.resolvers.packages import resolve_packages
from accountable_record.pipeline.types import PipelineStageError, StageResult

STAGE_ID = "s070"
STAGE_CODE = "LK"
STAGE_TITLE = "Resolve packages and write lock material"


def resolve_only(root: Path) -> StageResult:
    """Resolve package element references without writing the lock."""
    result = resolve_packages(root)
    if result.errors:
        raise PipelineStageError(STAGE_ID, STAGE_CODE, "; ".join(result.errors))

    return StageResult(
        STAGE_ID,
        STAGE_CODE,
        f"resolved {len(result.packages)} package(s) to "
        f"{len(result.elements)} unique element(s)",
    )


def write_only(root: Path) -> StageResult:
    """Write data/locks/elements.lock.json."""
    result = write_lock(root)
    if result.errors:
        raise PipelineStageError(STAGE_ID, STAGE_CODE, "; ".join(result.errors))

    return StageResult(STAGE_ID, STAGE_CODE, "wrote data/locks/elements.lock.json")


def run(root: Path) -> StageResult:
    """Resolve package references and write lock material."""
    resolve_only(root)
    write_result = write_only(root)

    return StageResult(
        STAGE_ID,
        STAGE_CODE,
        write_result.message,
    )
