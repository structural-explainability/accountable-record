"""Pipeline stage s010: validate repository identity metadata."""

from pathlib import Path

from se_contract_kit.declarations.config import load_repo_config

from accountable_record.pipeline.types import PipelineStageError, StageResult

STAGE_ID = "s010"
STAGE_CODE = "ID"
STAGE_TITLE = "Validate repository identity metadata"


def run(root: Path) -> StageResult:
    """Load repository declarations and confirm identity metadata is readable."""
    try:
        load_repo_config(repo_root=root)
    except Exception as exc:  # noqa: BLE001
        raise PipelineStageError(
            STAGE_ID,
            STAGE_CODE,
            f"repository identity metadata could not be loaded: {exc}",
        ) from exc

    return StageResult(STAGE_ID, STAGE_CODE, "repository identity metadata loaded")
