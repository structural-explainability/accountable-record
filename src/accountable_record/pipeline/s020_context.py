"""Pipeline stage s020: establish and validate contract context."""

from pathlib import Path

from se_contract_kit.declarations.config import load_repo_config
from se_contract_kit.resolution.resolver import resolve_repo_config

from accountable_record.pipeline.types import PipelineStageError, StageResult

STAGE_ID = "s020"
STAGE_CODE = "CT"
STAGE_TITLE = "Establish and validate contract context"


def run(root: Path) -> StageResult:
    """Resolve repository declarations into a contract resolution context."""
    try:
        config = load_repo_config(repo_root=root)
        resolve_repo_config(repo_root=root, config=config)
    except Exception as exc:  # noqa: BLE001
        raise PipelineStageError(
            STAGE_ID,
            STAGE_CODE,
            f"contract context could not be resolved: {exc}",
        ) from exc

    return StageResult(STAGE_ID, STAGE_CODE, "contract context resolved")
