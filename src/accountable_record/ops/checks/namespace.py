"""Namespace authority and alias resolution checks, as a kit Check record.

WHY (AR-D-004): namespace authorities own their project spaces. Compact ids
require alias resolution. This check confirms every authority alias used in the
namespace data resolves to a declared authority, and that the alias and
authority tables agree with one another. AR-specific; appended to the kit
registry via registry.extend.

Converted from (root: Path) -> list[str] to the kit Check contract.
"""

from collections.abc import Iterable
from pathlib import Path
import tomllib

from se_contract_kit.resolution.context import ResolutionContext
from se_contract_kit.validation.registry import Check
from se_contract_kit.validation.results import CheckResult, cannot_verify, failure, ok

__all__ = ["CHECK_ID", "check_authority_aliases_resolve", "AUTHORITY_ALIASES_CHECK"]

CHECK_ID = "ar.namespace.authority-aliases-resolve"


def _load_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def check_authority_aliases_resolve(
    context: ResolutionContext,
) -> Iterable[CheckResult]:
    """Authority aliases and authorities must be mutually consistent."""
    root = context.repo_root
    aliases_path = root / "data" / "namespace" / "authority-aliases.toml"
    authorities_path = root / "data" / "namespace" / "authorities.toml"

    # WHY: with either file absent the cross-check cannot run -> cannot-verify.
    missing = [
        str(p.relative_to(root).as_posix())
        for p in (aliases_path, authorities_path)
        if not p.is_file()
    ]
    if missing:
        return [
            cannot_verify(CHECK_ID, f"missing namespace data: {', '.join(missing)}")
        ]

    try:
        aliases_data = _load_toml(aliases_path)
        authorities_data = _load_toml(authorities_path)
    except tomllib.TOMLDecodeError as exc:
        return [cannot_verify(CHECK_ID, f"invalid TOML in namespace data: {exc}")]

    results: list[CheckResult] = []

    alias_map: dict[str, str] = {}
    aliases = aliases_data.get("aliases")
    if not isinstance(aliases, list):
        return [
            cannot_verify(
                CHECK_ID, "authority-aliases.toml must define [[aliases]] rows"
            )
        ]
    for index, row in enumerate(aliases, start=1):
        if not isinstance(row, dict):
            results.append(failure(CHECK_ID, f"alias row {index} is not a table"))
            continue
        alias = row.get("alias")
        authority = row.get("authority")
        if not isinstance(alias, str) or not isinstance(authority, str):
            results.append(
                failure(CHECK_ID, f"alias row {index} missing alias/authority")
            )
            continue
        alias_map[alias] = authority

    authority_alias_map: dict[str, str] = {}
    authorities = authorities_data.get("authorities")
    if not isinstance(authorities, list):
        return [
            cannot_verify(CHECK_ID, "authorities.toml must define [[authorities]] rows")
        ]
    for index, row in enumerate(authorities, start=1):
        if not isinstance(row, dict):
            results.append(failure(CHECK_ID, f"authority row {index} is not a table"))
            continue
        authority = row.get("authority")
        alias = row.get("authority_alias")
        if not isinstance(authority, str):
            results.append(
                failure(CHECK_ID, f"authority row {index} missing authority")
            )
            continue
        if isinstance(alias, str):
            authority_alias_map[alias] = authority

    for alias, authority in alias_map.items():
        resolved = authority_alias_map.get(alias)
        if resolved is None:
            results.append(
                failure(
                    CHECK_ID, f"alias {alias!r} is not declared in authorities.toml"
                )
            )
        elif resolved != authority:
            results.append(
                failure(
                    CHECK_ID,
                    f"alias {alias!r} maps to {authority!r} in aliases but {resolved!r} in authorities",
                )
            )

    return results or [ok(CHECK_ID, "authority aliases and authorities are consistent")]


AUTHORITY_ALIASES_CHECK = Check(
    CHECK_ID, "Authority aliases resolve", check_authority_aliases_resolve
)
