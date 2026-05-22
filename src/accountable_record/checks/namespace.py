"""Namespace authority and alias resolution checks.

WHY (AR-D-004): namespace authorities own their project spaces. Compact ids
require alias resolution. These checks confirm that every authority alias used
in the namespace data resolves to a declared authority, and that the alias and
authority tables agree with one another.
"""

from pathlib import Path
import tomllib


def _load_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def check_authority_aliases_resolve(root: Path) -> list[str]:
    """Authority aliases and authorities must be mutually consistent."""
    aliases_path = root / "data" / "namespace" / "authority-aliases.toml"
    authorities_path = root / "data" / "namespace" / "authorities.toml"

    failures: list[str] = []

    if not aliases_path.is_file():
        failures.append("missing data/namespace/authority-aliases.toml")
    if not authorities_path.is_file():
        failures.append("missing data/namespace/authorities.toml")
    if failures:
        return failures

    try:
        aliases_data = _load_toml(aliases_path)
        authorities_data = _load_toml(authorities_path)
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid TOML in namespace data: {exc}"]

    # Map alias -> authority from the aliases table.
    alias_map: dict[str, str] = {}
    aliases = aliases_data.get("aliases")
    if not isinstance(aliases, list):
        failures.append("authority-aliases.toml must define [[aliases]] rows")
    else:
        for index, row in enumerate(aliases, start=1):
            if not isinstance(row, dict):
                failures.append(f"alias row {index} is not a table")
                continue
            alias = row.get("alias")
            authority = row.get("authority")
            if not isinstance(alias, str) or not isinstance(authority, str):
                failures.append(f"alias row {index} missing alias/authority")
                continue
            alias_map[alias] = authority

    # Map authority_alias -> authority from the authorities table.
    authority_alias_map: dict[str, str] = {}
    authorities = authorities_data.get("authorities")
    if not isinstance(authorities, list):
        failures.append("authorities.toml must define [[authorities]] rows")
    else:
        for index, row in enumerate(authorities, start=1):
            if not isinstance(row, dict):
                failures.append(f"authority row {index} is not a table")
                continue
            authority = row.get("authority")
            alias = row.get("authority_alias")
            if not isinstance(authority, str):
                failures.append(f"authority row {index} missing authority")
                continue
            if isinstance(alias, str):
                authority_alias_map[alias] = authority

    # Cross-check: every alias in the aliases table must agree with authorities.
    for alias, authority in alias_map.items():
        resolved = authority_alias_map.get(alias)
        if resolved is None:
            failures.append(f"alias {alias!r} is not declared in authorities.toml")
        elif resolved != authority:
            failures.append(
                f"alias {alias!r} maps to {authority!r} in aliases but "
                f"{resolved!r} in authorities"
            )

    return failures
