"""Identity / change / package contract shape checks, as a kit Check record.

WHY: The contract files under ``data/contracts/`` carry the load-bearing
identity principles (authority-based, version-free identity). This check
confirms the principles that DECISIONS.md and the README rely on are actually
asserted in the data, so the narrative cannot drift from the source.
AR-specific; appended to the kit registry via registry.extend.
"""

from collections.abc import Iterable
import tomllib

from se_contract_kit.resolution.context import ResolutionContext
from se_contract_kit.validation.registry import Check
from se_contract_kit.validation.results import (
    CheckResult,
    cannot_verify,
    failure,
    ok,
)

__all__ = ["CHECK_ID", "check_identity_contract_shape", "IDENTITY_CONTRACT_CHECK"]

CHECK_ID = "ar.contracts.identity-shape"


def check_identity_contract_shape(context: ResolutionContext) -> Iterable[CheckResult]:
    """The identity contract must assert version-free, authority-based identity."""
    path = context.repo_root / "data" / "contracts" / "identity-contract.toml"
    if not path.is_file():
        # WHY: contract file absent -> cannot run; we do not know whether the
        # principles hold. cannot-verify, not fail.
        return [
            cannot_verify(CHECK_ID, "missing data/contracts/identity-contract.toml")
        ]

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return [
            cannot_verify(CHECK_ID, f"invalid TOML in identity-contract.toml: {exc}")
        ]

    results: list[CheckResult] = []

    principles = data.get("principles")
    if not isinstance(principles, dict):
        results.append(
            failure(CHECK_ID, "identity-contract.toml must define [principles]")
        )
    else:
        for key in (
            "identity_is_authority_based",
            "canonical_identity_does_not_include_version",
            "released_identifiers_must_not_be_renamed",
        ):
            if principles.get(key) is not True:
                results.append(
                    failure(CHECK_ID, f"identity principle {key} must be true")
                )

    element_identity = data.get("element_identity")
    if not isinstance(element_identity, dict):
        results.append(
            failure(CHECK_ID, "identity-contract.toml must define [element_identity]")
        )
    else:
        if element_identity.get("package_independent") is not True:
            results.append(
                failure(CHECK_ID, "element_identity.package_independent must be true")
            )
        if element_identity.get("element_id_must_not_include_package_id") is not True:
            results.append(
                failure(
                    CHECK_ID,
                    "element_identity.element_id_must_not_include_package_id must be true",
                )
            )

    return results or [ok(CHECK_ID, "identity contract shape valid")]


IDENTITY_CONTRACT_CHECK = Check(
    CHECK_ID, "Identity contract shape", check_identity_contract_shape
)
