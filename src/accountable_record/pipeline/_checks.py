"""Helpers for running kit-compatible checks from pipeline stages."""

from collections.abc import Iterable
from pathlib import Path

from se_contract_kit.declarations.config import load_repo_config
from se_contract_kit.resolution.resolver import resolve_repo_config
from se_contract_kit.validation import run_checks
from se_contract_kit.validation.registry import Check, CheckRegistry

from accountable_record.pipeline.types import PipelineStageError


def run_stage_checks(
    root: Path,
    *,
    stage_id: str,
    code: str,
    checks: Iterable[Check],
    strict: bool = False,
) -> int:
    """Run a stage-specific set of kit checks.

    Args:
        root: Repository root.
        stage_id: Pipeline stage id.
        code: Pipeline stage code.
        checks: Checks to run for this stage.
        strict: Whether strict checks should be enabled.

    Returns:
        Number of check results produced.

    Raises:
        PipelineStageError: If any selected check fails.
    """
    config = load_repo_config(repo_root=root)
    context = resolve_repo_config(repo_root=root, config=config)

    registry = CheckRegistry().extend(*tuple(checks))
    report = run_checks(registry=registry, context=context, strict=strict)

    if report.passed:
        return len(report.results)

    messages = []
    for item in report.failures:
        location = f" [{item.artifact_id}]" if item.artifact_id else ""
        messages.append(f"{item.check_id}{location}: {item.message}")

    raise PipelineStageError(stage_id, code, "; ".join(messages))
