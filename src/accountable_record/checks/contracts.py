"""Identity / change / package contract shape checks.

WHY: The three contract files under ``data/contracts/`` carry the load-bearing
identity principles (authority-based, version-free identity). These checks
confirm the principles that DECISIONS.md and the README rely on are actually
asserted in the data, so the narrative cannot drift from the source.
"""

from pathlib import Path
import tomllib


def _load_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def check_identity_contract_shape(root: Path) -> list[str]:
    """The identity contract must assert version-free, authority-based identity."""
    path = root / "data" / "contracts" / "identity-contract.toml"
    if not path.is_file():
        return ["missing data/contracts/identity-contract.toml"]

    try:
        data = _load_toml(path)
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid TOML in identity-contract.toml: {exc}"]

    failures: list[str] = []

    principles = data.get("principles")
    if not isinstance(principles, dict):
        failures.append("identity-contract.toml must define [principles]")
    else:
        required_true = [
            "identity_is_authority_based",
            "canonical_identity_does_not_include_version",
            "released_identifiers_must_not_be_renamed",
        ]
        for key in required_true:
            if principles.get(key) is not True:
                failures.append(f"identity principle {key} must be true")

    element_identity = data.get("element_identity")
    if not isinstance(element_identity, dict):
        failures.append("identity-contract.toml must define [element_identity]")
    else:
        if element_identity.get("package_independent") is not True:
            failures.append("element_identity.package_independent must be true")
        if element_identity.get("element_id_must_not_include_package_id") is not True:
            failures.append(
                "element_identity.element_id_must_not_include_package_id must be true"
            )

    return failures
