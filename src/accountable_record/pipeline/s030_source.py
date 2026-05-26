"""Pipeline stage s030: validate repository source materials."""

from pathlib import Path

from accountable_record.ops.checks.conformance import AR_CONFORMANCE_CHECKS
from accountable_record.ops.checks.contracts import IDENTITY_CONTRACT_CHECK
from accountable_record.ops.checks.namespace import AUTHORITY_ALIASES_CHECK
from accountable_record.ops.checks.records import RECORD_MATURITY_CHECK
from accountable_record.ops.checks.schemas import AR_SCHEMAS_CHECK
from accountable_record.ops.checks.source import AR_SOURCE_CHECKS
from accountable_record.pipeline._checks import run_stage_checks
from accountable_record.pipeline.types import StageResult

STAGE_ID = "s030"
STAGE_CODE = "SR"
STAGE_TITLE = "Validate repository source materials"


def run(root: Path) -> StageResult:
    """Validate authored repository source artifacts."""
    result_count = run_stage_checks(
        root,
        stage_id=STAGE_ID,
        code=STAGE_CODE,
        checks=(
            *AR_SOURCE_CHECKS,
            AR_SCHEMAS_CHECK,
            *AR_CONFORMANCE_CHECKS,
            AUTHORITY_ALIASES_CHECK,
            IDENTITY_CONTRACT_CHECK,
            RECORD_MATURITY_CHECK,
        ),
    )

    return StageResult(
        STAGE_ID,
        STAGE_CODE,
        f"repository source materials passed {result_count} check result(s)",
    )
