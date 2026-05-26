"""Pipeline stage s040: validate verifiable element declarations."""

from pathlib import Path

from accountable_record.ops.checks.component_groups import GROUP_INDEX_CHECK
from accountable_record.ops.checks.elements import AR_ELEMENT_CHECKS
from accountable_record.pipeline._checks import run_stage_checks
from accountable_record.pipeline.types import StageResult

STAGE_ID = "s040"
STAGE_CODE = "EL"
STAGE_TITLE = "Validate verifiable element declarations"


def run(root: Path) -> StageResult:
    """Validate component groups, element declarations, and element locks."""
    result_count = run_stage_checks(
        root,
        stage_id=STAGE_ID,
        code=STAGE_CODE,
        checks=(GROUP_INDEX_CHECK, *AR_ELEMENT_CHECKS),
    )

    return StageResult(
        STAGE_ID,
        STAGE_CODE,
        f"verifiable element declarations passed {result_count} check result(s)",
    )
