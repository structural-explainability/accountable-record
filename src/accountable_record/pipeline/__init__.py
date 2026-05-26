"""Staged Accountable Record pipeline.

WHY: The staged pipeline is the human-facing lifecycle map for this repository.
Stages describe the ordered Accountable Record source-to-artifacts workflow.
Implementation mechanics stay in accountable_record.ops.
"""

from accountable_record.pipeline.registry import STAGE_BY_ID, STAGES
from accountable_record.pipeline.runner import run_all, run_stage

__all__ = ["STAGES", "STAGE_BY_ID", "run_all", "run_stage"]
