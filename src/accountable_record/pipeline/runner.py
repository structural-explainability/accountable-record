"""Run Accountable Record pipeline stages."""

from pathlib import Path

from accountable_record.pipeline.registry import STAGE_BY_ID, STAGES
from accountable_record.pipeline.types import PipelineStageError, StageResult


def _print_success(result: StageResult) -> None:
    print(f"[{result.stage_id} {result.code}] ok  {result.message}")


def run_stage(stage_id: str, root: Path) -> int:
    """Run one registered pipeline stage.

    Args:
        stage_id: Stage id, such as ``s050``.
        root: Repository root.

    Returns:
        Process exit code.
    """
    stage = STAGE_BY_ID.get(stage_id)
    if stage is None:
        valid = ", ".join(sorted(STAGE_BY_ID))
        print(f"Unknown stage {stage_id!r}. Valid stages: {valid}")
        return 2

    try:
        result = stage.run(root)
    except PipelineStageError as exc:
        print(f"[{exc.stage_id} {exc.code}] FAIL  {exc.message}")
        return 1

    _print_success(result)
    return 0


def run_all(root: Path) -> int:
    """Run all registered pipeline stages in order.

    Args:
        root: Repository root.

    Returns:
        Process exit code.
    """
    for stage in STAGES:
        try:
            result = stage.run(root)
        except PipelineStageError as exc:
            print(f"[{exc.stage_id} {exc.code}] FAIL  {exc.message}")
            print(f"Pipeline stopped at {exc.stage_id} ({exc.code}).")
            return 1

        _print_success(result)

    return 0
