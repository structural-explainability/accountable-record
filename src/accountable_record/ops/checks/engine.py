"""Accountable-record check registry: extend the kit's defaults with AR's checks.

WHY: se-contract-kit owns the generic checks (resolved-artifact existence,
provide-or-consume, vocabulary closure) and the engine that runs them. AR
supplies its own DOMAIN checks -- which know AR's file layout, interchange
schemas, conformance vocabulary, element-identity rule, and working-draft
policy -- and appends them to the kit's default registry via the registry's
immutable extension seam. The kit is never forked or edited; it is extended.

Each AR check module owns its Check records and exposes them as a tuple (or a
single Check). This module's only job is to gather those in a stable order and
hand the combined set to the kit. It constructs no Check objects itself, so
check metadata (id, title, strict-ness) lives next to each implementation.

REQ: check_ids are stable; CI logs and tests reference them.
NOTE: AR registers its OWN strict no-TODO check, which permits TODO in drafts
and forbids it only at release. The kit's generic no-TODO check is intentionally
NOT included -- it would wrongly flag AR's legitimate draft elements.
"""

from se_contract_kit.validation import CheckRegistry, default_registry
from se_contract_kit.validation.registry import Check

from accountable_record.ops.checks.component_groups import GROUP_INDEX_CHECK
from accountable_record.ops.checks.conformance import AR_CONFORMANCE_CHECKS
from accountable_record.ops.checks.contracts import IDENTITY_CONTRACT_CHECK
from accountable_record.ops.checks.elements import AR_ELEMENT_CHECKS
from accountable_record.ops.checks.namespace import AUTHORITY_ALIASES_CHECK
from accountable_record.ops.checks.records import RECORD_MATURITY_CHECK
from accountable_record.ops.checks.schemas import AR_SCHEMAS_CHECK
from accountable_record.ops.checks.source import AR_SOURCE_CHECKS
from accountable_record.ops.checks.strict import AR_STRICT_CHECKS

__all__ = ["AR_CHECKS", "accountable_record_registry"]

# WHY: ordered so foundational problems (missing/unparseable source) surface
# before higher-level cross-reference failures, matching the legacy engine's
# intent. Strict-only checks (AR_STRICT_CHECKS) sort last; the runner skips
# them unless strict mode is requested.
AR_CHECKS: tuple[Check, ...] = (
    *AR_SOURCE_CHECKS,
    AR_SCHEMAS_CHECK,
    *AR_CONFORMANCE_CHECKS,
    GROUP_INDEX_CHECK,
    *AR_ELEMENT_CHECKS,
    AUTHORITY_ALIASES_CHECK,
    IDENTITY_CONTRACT_CHECK,
    RECORD_MATURITY_CHECK,
    *AR_STRICT_CHECKS,
)


def accountable_record_registry() -> CheckRegistry:
    """Return the kit's default registry extended with AR's domain checks."""
    return default_registry().extend(*AR_CHECKS)
