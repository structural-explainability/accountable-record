from pathlib import Path

from se_contract_kit.declarations.config import load_repo_config
from se_contract_kit.resolution.resolver import resolve_repo_config
from se_contract_kit.validation import run_checks
from se_contract_kit.validation.registry import Check

from accountable_record.ops.checks.engine import accountable_record_registry


def _context_for(root: Path):
    config = load_repo_config(repo_root=root)
    return resolve_repo_config(repo_root=root, config=config)


def _messages_for_check(root: Path, check: Check) -> list[str]:
    context = _context_for(root)
    report = run_checks(
        registry=accountable_record_registry().extend(check),
        context=context,
        strict=True,
    )
    return [failure.message for failure in report.failures]
